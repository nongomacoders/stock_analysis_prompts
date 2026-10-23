# Section 18: Alternative performance measures — ADJUSTED EBITDA

> **Package**: `section-b79e63c1a07c44718ea7d02595b3afee`  
> **Report**: `Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf` (annual_report)  
> **Model**: `deepseek/deepseek-v4.1-flash-1017`  
> **Execution Time**: 359.34s  
> **Cost**: $0.0047  
> **Tokens**: 23,067 total (12,326 prompt / 10,741 completion)  

### 1. Answers to Stored Questions for This Section

**Q119: Locate Adjusted EBITDA reconciliation; confirm SBP NOT added back, STI FV gain added back, impairment quantum, FY25 restated 252,678.**
- **Status**: `Partially resolved (remainder stays open for D006.2 / D006.5)`
- **Answer & evidence**: The by-operation reconciliation is on `[D008.4, physical PDF p. 45]`. It starts from "Net income/(cost) before finance income and finance costs" and adds back "Mining depreciation and amortisation" and "(Profit)/loss on disposal of plant and equipment" to reach Adjusted EBITDA. **No share-based payment (SBP) line appears** — consistent with SBP NOT being added back. **No STI fair-value gain line appears** in the FY26 reconciliation (only an "Unrealised fair value loss on financial derivatives" line of 1.9 in FY25), so the STI FV gain add-back is not evidenced here and remains open. **No impairment line appears** in either year's reconciliation, so the impairment quantum is not evidenced here. The FY25 "Adjusted EBITDA" group total in this table is **245.8**, not the 252,678 (US$252.7m) referenced in Q119 — a discrepancy to resolve against the Note 3 reconciliation. `[D008.4, p. 45]`

**Q128: Confirm STI (137,867) and gold trading (58,931) classified as "normal course" derivatives for Adjusted EBITDA add-back.**
- **Status**: `Partially resolved (remainder stays open for D008.1 / D006.10)`
- **Answer & evidence**: The definition on `[D008.4, p. 45]` excludes only "unrealised fair value loss on financial derivatives" from Adjusted EBITDA; the "Net Adjusted EBITDA" definition on `[D008.4, p. 46]` adjusts for "unrealised fair value gains or losses on financial derivatives that are entered into in the normal course of business as part of the Group's financial risk management process." This confirms the *mechanism* for a normal-course derivative add-back but does **not** confirm the specific STI (137,867) or gold trading (58,931) amounts are so classified. Remains open.

**Q131: Confirm rehab fund FV gain treatment in Adjusted EBITDA.**
- **Status**: `Partially resolved (remainder stays open for D006.10)`
- **Answer & evidence**: The Adjusted EBITDA definition `[D008.4, p. 45]` excludes "unrealised fair value loss on financial derivatives" and "impairment of non-financial assets, bargain purchase gain" but makes **no mention of rehabilitation fund fair-value gains/losses**. The reconciliation table `[D008.4, p. 45]` shows no rehab-fund line. So there is no evidence the rehab fund FV gain is added back/excluded — it appears to remain inside "Net income before finance income and finance costs." Remains open for confirmation against Note 10/Note 19.

**Q121: Locate FCF reconciliation; identify "permitted indebtedness"-funded capex and IAS 7 non-cash adjustments; reconcile to cash flow statement.**
- **Status**: `Partially resolved (definition located; reconciliation not in this capture)`
- **Answer & evidence**: The FCF *definition* is on `[D008.4, p. 46]`: "starts with adjusted EBITDA and is adjusted for changes in net working capital, non-cash flow items as determined by IAS 7, capital expenditure less capital funded through permitted indebtedness and tax payments." The actual FCF reconciliation table is **not present** in this capture (only the Levered FCF table is shown). Remains open.

**Q122: Locate LFCF reconciliation; confirm RCF repayment (30 June 2027 maturity) modelled; tie to net debt movement.**
- **Status**: `Resolved (reconciliation located)`
- **Answer & evidence**: Levered FCF reconciliation on `[D008.4, p. 46]`: Adjusted EBITDA 609.4 − finance costs paid 15.0 − income tax paid 74.1 + net working capital movement 46.6 − capex 215.8 + proceeds from borrowings 0 − repayment of borrowings 149.3 = **LFCF 201.8** (FY25: 47.5). Note the LFCF starting Adjusted EBITDA is **609.4**, which differs from the by-operation table's 663.1 `[D008.4, p. 45]` — a reconciliation gap to resolve. RCF maturity/repayment modelling is not evidenced here; remains open for D006.8.

**Q123: Locate headline earnings reconciliation; confirm disposal/impairment/tax adjustments and EPS denominator.**
- **Status**: `Partially resolved (definition only)`
- **Answer & evidence**: Only the *definition* is on `[D008.4, p. 46]`: "Headline earnings, a JSE-defined performance measure (as defined by Circular 2023/1 issued by SAICA), are reconciled from profit/(loss) after tax in note 13." The actual reconciliation is **not in this capture**. EPS denominator: shares in issue 2,333.7m less treasury 306.4m = **2,027.3m** used for attributable cash flow per share `[D008.4, p. 46]`. Remains open for Note 13.

**Q132: Identify IAS 7 non-cash items adjusted in FCF; confirm SBP treatment in FCF.**
- **Status**: `Partially resolved (definition only)`
- **Answer & evidence**: FCF definition references "non-cash flow items as determined by IAS 7" `[D008.4, p. 46]` but the itemised reconciliation is not in this capture. SBP treatment in FCF not evidenced. Remains open.

**Q86 (remainder): Confirm RCF renewal/refinancing plans before 30 June 2027 maturity; FY27 liquidity headroom.**
- **Status**: `Partially resolved (indirect)`
- **Answer & evidence**: LFCF table shows FY26 "Repayment of borrowings 149.3" and "Proceeds from borrowings –" `[D008.4, p. 46]`, i.e., net debt repayment in FY26 with no new drawdowns. No RCF maturity/refinancing commentary in this capture. Remains open for D006.8.

**Q81 (remainder): Confirm STI FV gain US$1,142k excluded from Adjusted EBITDA/AISC.**
- **Status**: `Partially resolved (mechanism only)`
- **Answer & evidence**: Net Adjusted EBITDA definition adjusts for normal-course derivative FV gains/losses `[D008.4, p. 46]`; the specific 1,142 STI gain is not shown in this capture. Remains open.

**Q36 (remainder): Confirm FY25 restated Adjusted EBITDA 252,678.**
- **Status**: `Contradicted / discrepancy found`
- **Answer & evidence**: The by-operation table shows FY25 group Adjusted EBITDA of **245.8** `[D008.4, p. 45]`, and the LFCF table shows FY25 Adjusted EBITDA of **226.6** `[D008.4, p. 46]`. Neither equals 252,678 (US$252.7m). Three different FY25 Adjusted EBITDA figures now exist — must be reconciled to Note 3. Remains open.

*(Stored questions belonging to other sections not evidenced here are carried forward in Section 4.)*

### 2. Footnote & Qualification Deep-Dive

- **Footnote `[^1]` on p. 46 (LFCF yield):** "Amounts converted at the 30 June 2026 closing exchange rate of US$/ZAR:16.46 (FY25: US$/ZAR:17.75)." This is the FX rate used to convert the last traded price (125.09 US cents) and hence the 7.96% cash flow yield. **Implication:** the yield is FX-sensitive; a weaker ZAR inflates the US-cent share price and yield. Note this 16.46 close rate differs from the 16.90 average used elsewhere (Q4) — confirm which rate underpins FY27 dividend/FX assumptions. `[D008.4, p. 46]`

- **Footnote `[^1]` on p. 47 (dividend yield):** "Includes the maiden interim dividend of ZA 12.00 cents (0.55 pence) per share." **Implication:** FY26 DPS of 77.00 ZA cents is the *full-year* figure including the maiden interim; the FY26 dividend is therefore not a clean run-rate for FY27 unless the interim is annualised. Must confirm FY27 dividend policy and whether 77.00 is a sustainable base. `[D008.4, p. 47]`

- **Embedded qualification — Adjusted EBITDA definition (p. 45):** Excludes "impairment of non-financial assets, bargain purchase gain and unrealised fair value loss on financial derivatives." **Implication:** the FY25 bargain gain of (28.0) at Tennant is added back to reach FY25 Adjusted EBITDA of 2.4 for Tennant `[D008.4, p. 45]` — i.e., Tennant's FY25 underlying operating contribution was near-zero once the one-off bargain gain is stripped. This is a critical base-effect caveat for FY27 Tennant forecasting.

- **Embedded qualification — Net Adjusted EBITDA (p. 46):** Adjusts for normal-course derivative FV gains/losses. **Implication:** creates a second EBITDA layer (net adjusted) used for leverage/interest cover ratios; must confirm which EBITDA (adjusted 663.1 vs 609.4 vs net adjusted) feeds the net debt/EBITDA and interest cover ratios.

- **Arithmetic tension flagged:** By-operation Adjusted EBITDA group total **663.1** `[p. 45]` vs LFCF starting Adjusted EBITDA **609.4** `[p. 46]` — a **53.7** gap. Also FY25: 245.8 vs 226.6 = **19.2** gap. These must be reconciled (likely corporate costs / net adjusted derivative adjustments) before using either as the forecast base.

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| Q157 | High | D006.2 (Note 3 Segment) | By-operation Adjusted EBITDA group total 663.1 `[D008.4, p. 45]` vs LFCF starting Adjusted EBITDA 609.4 `[D008.4, p. 46]` — 53.7 gap | Locate Note 3 Adjusted EBITDA reconciliation; identify the reconciling items (corporate/unallocated costs, net adjusted derivative adjustments) bridging 663.1 to 609.4 | Determines the correct EBITDA base for FY27 forecast and leverage ratios |
| Q158 | High | D006.2 (Note 3 Segment) | FY25 Adjusted EBITDA appears as 245.8 `[p. 45]`, 226.6 `[p. 46]`, and 252,678 per Q36/Q119 | Reconcile all three FY25 figures to the Note 3 restated reconciliation; confirm which is the audited restated number | Base-year integrity for YoY growth and margin forecast |
| Q159 | High | D006.2 (Note 3 Segment) | No impairment line in Adjusted EBITDA reconciliation `[D008.4, p. 45]` despite Q119 expecting one | Confirm whether any FY26 impairment exists and where it sits (P&L vs excluded from Adjusted EBITDA); quantify | Impairment affects headline earnings, NAV, and possibly debt covenants |
| Q160 | High | D006.10 / D006.9 | STI FV gain (137,867) and gold trading (58,931) not visible in reconciliation `[D008.4, p. 45–46]` | Confirm whether STI/gold trading FV movements are inside "Net income before finance costs" and whether added back in Net Adjusted EBITDA; quantify FY26 FV gain/loss | Affects Adjusted EBITDA quality and net debt treatment (Q108/Q120) |
| Q161 | Medium | D006.10 (Note 19/20) | Rehab fund FV gain not referenced in Adjusted EBITDA definition `[D008.4, p. 45]` | Confirm rehab fund FV gain/loss FY26 amount and whether it sits in "Net income before finance costs" (i.e., NOT added back) | Determines whether Adjusted EBITDA is inflated by non-cash rehab FV gains |
| Q162 | Medium | D006.2 / D006.5 | Tennant FY25 Adjusted EBITDA only 2.4 after adding back bargain gain (28.0) `[D008.4, p. 45]` | Confirm Tennant FY25 underlying operating result and FY26 43.0 build; isolate one-offs | Critical base-effect for FY27 Tennant ramp forecast |
| Q163 | Medium | D006.8 (Note 15/16) | LFCF shows repayment of borrowings 149.3, proceeds nil `[D008.4, p. 46]` | Confirm RCF maturity 30 June 2027, refinancing plan, and FY27 debt service obligations feeding debt service cover ratio | Liquidity/refinancing risk and FY27 finance cost forecast |
| Q164 | Medium | D006.2 / D005 | Adjusted EBITDA margin and gross profit margin definitions given but no values `[D008.4, p. 47]` | Extract revenue and gross profit to compute FY26/FY25 margins; confirm revenue base for 663.1 EBITDA | Margin trajectory for FY27 forecast |
| Q165 | Low | D006.11 / D002 | FY26 DPS 77.00 includes maiden interim 12.00 `[D008.4, p. 47, fn 1]` | Confirm FY27 dividend policy and whether 77.00 is annualised run-rate; confirm payout ratio vs LFCF 201.8 | Dividend forecast and cash flow to shareholders |
| Q166 | Low | D006.2 / D006.5 | ROCE 59.8% uses "Net income before finance income and finance costs 545.8" `[D008.4, p. 47]` — differs from by-operation 602.2 `[p. 45]` | Reconcile 545.8 to 602.2 (corporate/unallocated); confirm average equity 791.3 and average borrowings 120.8 | Validates capital efficiency and debt base for forecast |

### 4. Updated Open Questions Ledger (Copy to App)

```markdown
# OPEN QUESTIONS LEDGER — after D008.4 (Adjusted EBITDA, pp. 45–47)

## Pending: D006.2 (Note 3 Segment Analysis) — HIGH PRIORITY
- Q157: Reconcile by-operation Adjusted EBITDA 663.1 [D008.4, p.45] to LFCF starting Adjusted EBITDA 609.4 [D008.4, p.46]; identify 53.7 gap (corporate/unallocated, net adjusted derivative adjustments).
- Q158: Reconcile FY25 Adjusted EBITDA appearing as 245.8 [p.45], 226.6 [p.46], and 252,678 [Q36/Q119]; confirm audited restated figure.
- Q159: Confirm whether any FY26 impairment exists and where it sits (P&L vs excluded from Adjusted EBITDA); quantify.
- Q162: Confirm Tennant FY25 underlying operating result (Adjusted EBITDA 2.4 after bargain gain 28.0 add-back) and FY26 43.0 build; isolate one-offs.
- Q164: Extract revenue and gross profit to compute FY26/FY25 Adjusted EBITDA margin and gross profit margin [D008.4, p.47 definitions].
- Q166: Reconcile ROCE numerator 545.8 [p.47] to by-operation 602.2 [p.45]; confirm average equity 791.3 and average borrowings 120.8.
- Q36 (remainder): Confirm FY25 restated Adjusted EBITDA 252,678 in reconciliation table. [D006.2, p.22,24; D008.1, p.38]
- Q42: Confirm segment AISC/APMs before or after intra-group management fee allocation. [D006.2, p.21]
- Q44: Reconcile segment net assets 1,017,559 + goodwill 18,438 = 1,035,997 to group total equity. [D006.2, p.22]
- Q65: Extract segment-level D&A from Note 3 to split Tennant/Emmerson vs SA. [D006.5, p.28]
- Q155: Confirm by-mine "Mining operations" sub-rows (Barberton 12.2/8.3; Evander –/–) are non-additive to mine totals; avoid double-count. [D008.3, p.44; D006.2, p.22]

## Pending: D006.10 / D006.9 (Notes 19,20,21 / 17,18) — HIGH PRIORITY
- Q160: Confirm STI FV gain (137,867) and gold trading (58,931) sit inside "Net income before finance costs" and whether added back in Net Adjusted EBITDA; quantify FY26 FV gain/loss.
- Q161: Confirm rehab fund FV gain/loss FY26 amount and whether it sits in "Net income before finance costs" (NOT added back).
- Q108 (remainder): Confirm STI 137,867 treatment in net debt; FY27 FV assumption. [D006.10, p.35–36; D008.1, p.38–39; D008.3, p.44]
- Q112 (remainder): Confirm rehab fund FV assumption and Adjusted EBITDA treatment; AISC shows reclamation accretion −0.6 (FY26). [D006.10, p.35–36; D008.2, p.40]
- Q143: Confirm rehab fund FV gain/loss treatment in Adjusted EBITDA; accretion stays negative in FY27. [D008.2, pp.40–41]
- Q81 (remainder): Confirm STI FV gain US$1,142k excluded from Adjusted EBITDA/AISC; confirm STI treatment in net debt. [D006.7, p.30; D006.10, p.35; D008.1, p.38–39]
- Q128: Confirm STI (137,867) and gold trading (58,931) classified as "normal course" derivatives for Adjusted EBITDA add-back. [D008.1, p.38]
- Q131: Confirm rehab fund FV gain treatment in Adjusted EBITDA. [D008.1, p.38]
- Q132: Identify IAS 7 non-cash items adjusted in FCF; confirm SBP treatment in FCF. [D008.1, p.39]
- Q121: Locate FCF reconciliation; identify "permitted indebtedness"-funded capex and IAS 7 non-cash adjustments; reconcile to cash flow statement. [D008.1, p.39]
- Q123: Locate headline earnings reconciliation (Note 13); confirm disposal/impairment/tax adjustments and EPS denominator. [D008.1, p.39]
- Q103: Identify missing ~43,831 FY26 adjustment line in Note 19 "Adjusted for" subtotal 143,482. [D006.10, p.35]
- Q109: Confirm FY27 payables unwind assumption; reconcile Note 19 trade and other payables increase 50,354 to D006.7 29,480. [D006.10, p.35; D006.7, p.30]
- Q105 (remainder): Identify projects for 309,076 board-approved commitments and 94,580 open orders; tie to FY27 capex. [D006.10, p.36; D008.2, p.40; D008.3, p.44]
- Q107: Quantify PPA with NOA Group (3 July 2025, 10+5 years) cost commitment and start date; FY27 electricity step-up. [D006.10, p.36; D008.1, p.39]
- Q114: Confirm AISC/electricity reflects external PPA only; quantify external electricity post solar disposal. [D006.11, p.36; D008.1, p.39]
- Q50 (remainder): Confirm restricted cash 2,612 nature; finance income 60 FY26 vs nil FY25; confirm inside cash 108.3. [D006.10, p.35; D008.1, p.39; D008.3, p.44]
- Q94 (remainder): Confirm exploration asset carrying value US$142,244k; FY27 depletion/impairment; AISC exclusion confirmed. [D006.9, p.34; D008.2, p.40]
- Q95 (remainder): Confirm Emmerson transaction costs US$11,879k capitalised (not in P&L/Adjusted EBITDA); no APM add-back. [D006.9, p.34; D008.2, p.40]
- Q96 (remainder): Reconcile Note 18.2 "no disposals" against solar disposal expectation; confirm timing/gain and FY27 electricity step-up. [D006.9, p.34; D008.1, p.39; D008.3, p.44]
- Q100 (remainder): Confirm cash-settled SBP current portion US$43,969k in net debt/liquidity; FY27 cash settlement. [D006.9, p.33; D006.10, p.35; D008.1, p.39; D008.3, p.44]
- Q102: Confirm PAR Gold G-share vesting/settlement (11,541,455, vest 30 June 2026) in FY27 cash flow; I-share FY27 expense. [D006.9, p.34; D008.1, p.38]
- Q152: Confirm SBP 43,969 sits in current liabilities (not debt); confirm FY27 cash settlement timing. [D008.3, p.44; D006.9, p.33; D006.10, p.35]
- Q153: Confirm restricted cash 2,612 is inside cash 108.3 and not "available" for senior debt netting. [D008.3, p.44; D006.10, p.35]

## Pending: D006.8 (Note 15/16 borrowings) — HIGH PRIORITY
- Q163: Confirm RCF maturity 30 June 2027, refinancing plan, and FY27 debt service obligations feeding debt service cover ratio.
- Q86 (remainder): Confirm RCF renewal/refinancing plans before 30 June 2027 maturity; FY27 liquidity headroom (net cash 185.7 improves headroom). [D006.8, p.31; D008.1, p.39; D008.3, p.44]
- Q122: Confirm RCF repayment (30 June 2027 maturity) modelled; tie LFCF 201.8 to net debt movement. [D008.1, p.39]
- Q87: Quantify JIBAR→ZARONIA interest rate impact; confirm ZARONIA vs JIBAR. [D006.8, pp.31–32; D008.1, p.39]
- Q146: Identify whether gold loan (25,557) and/or gold trading (58,931) sit inside "Borrowings 51.5", are netted in cash, or are excluded; reconcile to Note 15/16 borrowings. [D008.3, p.44; D006.8, p.31–33]
- Q147: Reconcile borrowings movement 138.5 to cash flow financing repayments 149.3; explain FX translation / IFRS 9 / new drawdowns. [D008.3, p.44; D006.8, pp.31–32; D006.10, p.35]
- Q150: Identify the 1.2 financial liability (SBP? other?); confirm lease 7.8 = IFRS 16 and FY27 lease payments. [D008.3, p.44]
- Q151: Confirm senior debt excludes leases and the 1.2 liability; confirm STI netted in both net debt and net senior debt. [D008.3, p.44]
- Q89 (remainder): Confirm gold loan 25,557 and gold trading 58,931 included/excluded from net debt. [D006.8, p.33; D008.1, p.39; D008.3, p.44]
- Q120 (remainder): Confirm treatment of gold loan 25,557, gold trading 58,931, STI 137,867, cash-settled SBP 43,969, restricted cash 2,612, IFRS 16 leases in net debt. [D008.1, p.39; D008.3, p.44]
- Q129 (remainder): Confirm which financial liabilities added to net debt (SBP? gold loan? trading?). [D008.1, p.39; D008.3, p.44]
- Q130 (remainder): Confirm "cash and related hedges" meaning; whether STI netted in net debt. [D008.1, p.39; D008.3, p.44]
- Q84 (remainder): Check cash flow statement financing activities for total debt repayments US$149,311k; reconcile to net debt movement. [D006.8, pp.31–32; D006.10, p.35; D008.3, p.44]
- Q47 (remainder): Check FY27 capex interest-capitalisation; FY27 finance cost run-rate; DMTN coupon rates. [D006.4, p.25; D006.8, pp.31–32]

## Pending: D006.5 / D006.6 / D006.7 (PPE, inventory, SBP) — MEDIUM
- Q63 (remainder): Confirm AISC uses production D&A US$60,288k (not total PPE depreciation US$61,733k); identify US$2,179k "other D&A"; AISC reconciliation shows NO D&A line — resolve. [D006.5, p.28; D006.10, p.35; D008.2, p.40]
- Q64 (remainder): Confirm no further FY27 impairment; CGU headroom (Barberton land claim — Note 23). [D006.5, p.28; D006.11, p.36; D008.1, p.38]
- Q140: Locate production D&A in Note 3/Note 7; confirm whether inside cost of production 435.7 or excluded from AISC. [D008.2, p.40]
- Q67: Reconcile "Inventory recognised in cost of production" 57,468 vs 27,358 (+US$30,110k) to cost of sales in P&L and production volumes. [D006.6, p.29; D006.10, p.35]
- Q68: Check cyanide cost per tonne and prepayments 15,914 unwind in FY27; working capital movement. [D006.6, p.29]
- Q69: Check cash flow statement for VAT/GST receivable 18,107 timing and expected FY27 unwind. [D006.6, p.29; D006.10, p.35]
- Q72: Confirm solar projects status at FY26 year-end, disposal timing/gain, FY27 electricity step-up. [D006.6, p.29; D006.10, p.36; D006.11, p.36]
- Q75: Confirm nature/collectability of other receivables 7,828 (Evander/Barberton); loss allowance adequacy. [D006.6, p.29]
- Q25 (remainder): Extract FY26 SBP P&L charge and FY27 expected charge; explain "Other expenses" 85,958 vs 36,484. [D005.1, p.17–18; D006.2, p.21,23]
- Q12: Quantify SBP expense FY26 vs FY25 and FY27 assumption. [D002, p.3; D006.9, p.33]
- Q142: Confirm no FY27 voluntary severance / restructuring cost expected; check "Other expenses". [D008.2, pp.40–41]
- Q145: Confirm driver of corporate G&A step-up 18.7→34.9 and FY27 run-rate. [D008.2, pp.40–41]
- Q141: Map 309,076/94,580 commitments to specific projects (Tennant crusher/mill/filter, MTR expansion, White Devil) and FY27 timing. [D008.2, p.40]

## Pending: D006.4 (Income tax) — MEDIUM
- Q26 (remainder): FY27 expected effective tax rate — check D008/D009. [D006.1, p.19–20]
- Q32 (remainder): FY27 ETR from deferred tax note. [D006.1, p.19–20]
- Q39 (remainder): FY27 ETR, mining tax vs corporate tax split. [D006.2, p.21,23]
- Q52: Extract pre-tax profit from P&L; compute FY26/FY25 ETR; confirm 33.2%/28.5%. [D006.4, p.25]
- Q53: Confirm no remaining tax losses; model FY27 current tax at full statutory rates. [D006.4, p.26]
- Q57 (remainder): Confirm ZAR/AUD FX rate FY26 close vs FY25; FY27 FX sensitivity on DTL; averages 16.90/0.68 captured. [D006.4, p.26; D008.2, pp.42–43]
- Q58: Confirm Barberton deferred tax rate step 24.00%→28.29%; FY27 stability. [D006.4, p.26]

## Pending: D005.1 / D005 (Primary statements) — MEDIUM
- Q24 (remainder): Confirm reciprocal dividend (8,847) cash round-trip on 13.1% treasury; net vs gross; FY27 dividend policy. [D005.1, p.18–19; D006.7, p.30; D006.11, p.36]
- Q31 (remainder): Reconcile cash+STI US$246.2m (confirmed 108.3+137.9) and debt facilities US$78.9m (vs gross debt 60.5 here) to cash flow statement and Emmerson/equity issuance. [D006.1, p.19; D006.8, p.31,33; D006.10, p.35; D008.3, p.44]
- Q34 (remainder): Confirm APM reconciliation ties to IFRS — AISC starts from IFRS cost of production 435.7; tie to P&L cost of sales. [D008.2, p.40]
- Q77: Confirm FY27 weighted average share count including 102,641,421 Emmerson shares issued 1 July 2026; check EPS and DPS calculations. [D006.7, p.30; D006.9, p.34; D006.11, p.36]
- Q78: Confirm share buy-back cash cost (~US$1,322k) in cash flow statement financing activities; further buy-backs FY27. [D006.7, p.30]
- Q79: Confirm working capital movement for other payables +US$29,480k in cash flow statement; reconcile to Note 19 trade and other payables increase 50,354. [D006.7, p.30; D006.10, p.35]
- Q80: Confirm VAT payable US$5,836k payment timing in cash flow statement; jurisdiction. [D006.7, p.30]
- Q83 (remainder): Confirm treasury share treatment in EPS and dividend calculations; cancellation/reissue. [D006.7, p.30; D006.8, p.31]
- Q85: Check P&L net finance costs line; reconcile Note 19 finance costs 17,318 and income (4,706) = net 12,612 vs D006.8 gross 12,666 (4,652 gap). [D006.8, pp.31–32; D006.10, p.35]
- Q90: Check SOCIE for US$10,877k share premium cancellation reclassification to retained earnings; distributable reserves. [D006.8, p.31]
- Q92: Confirm 24,917,607 Tennant lender shares (issued FY25) in FY26 weighted average share count; EPS denominator. [D006.8, p.31, fn 1]
- Q93: Confirm 102,641,421 Emmerson shares excluded from 30 June 2026 issued count and included in FY27 weighted average from 1 July 2026; EPS/DPS denominators. [D006.9, p.34; D006.11, p.36]
- Q98: Confirm reserve for shares to be issued US$148,218k presented in equity (Note 14) and reconciles to SOCIE; no cash outflow. [D006.9, p.34]
- Q117: Confirm FY27 weighted average share count and EPS/DPS denominators include 102,641,421 Emmerson shares from 1 July 2026. [D006.11, p.36]
- Q149: Tie 51.5 borrowings and 108.3 cash to statement of financial position; quantify IFRS 9 adjustment and hedge asset netted in net debt definition. [D008.3, p.44; D005, p.17]

## Pending: D002 / D003 (Highlights / CEO statement) — MEDIUM
- Q3: Reconcile dividend implied share counts: 2,436m / 2,333m / 2,420m; issued/weighted count, Emmerson shares, treasury. [D002, p.2; D006.7, p.30; D006.9, p.34]
- Q4: Confirm FX rate/date for dividend US$ conversion (implied ~16.40–16.46 vs stated avg 16.90; note 16.46 close rate per D008.4 fn 1). [D002, p.2; D008.2, p.42; D008.4, p.46]
- Q8: Confirm Soweto Cluster DFS gold price assumption; FID timing Dec 2026; financing plan; capex post-FY27. [D002, p.3]
- Q11: Confirm renewable energy US$5.1m in FY26 base; water savings US$1.4m/yr incremental FY27+. [D002, p.2–3]
- Q16: Locate Tennant FY27 capex $ for fixed crusher, secondary mill, belt filter; capitalised vs expensed. [D003, p.6]
- Q19: Extract total FY27 group capex guidance and Tennant-specific split (FY26 actual 224.0 total / 202.2 expansion captured; APM expansion capex 195.0). [D003, p.6; D006.6, p.29; D008.2, p.40; D008.3, p.44]
- Q115: Confirm 8,847 reciprocal dividend is intra-group (eliminated), not external cash outflow; treasury-share mechanics. [D006.11, p.36]
- Q116: Confirm no provision/impairment for Barberton CGU or Evander litigation; contingent liability quantum. [D006.11, p.36]
- Q165: Confirm FY27 dividend policy and whether 77.00 DPS (incl. maiden interim 12.00) is annualised run-rate; payout ratio vs LFCF 201.8. [D008.4, p.47, fn 1]

## Pending: D009 (Group production summary) — HIGH PRIORITY
- Q1: Confirm total group ounces, Sheba+Consort ounces and AISC; reconcile to ~US$3,500/oz tail. [D002, p.2–3]
- Q5 (remainder): Confirm Tennant FY27 capex $; White Devil first blast date and grade ramp. [D002, p.3; D003, p.6]
- Q6 (remainder): Confirm Elikhulu/MTR full-year volumes — APM shows 57,092oz / 53,133oz sold vs stored 56,475oz / 51,927oz; reconcile production vs sold. [D008.2, p.42]
- Q7 (remainder): Confirm Evander underground grade >11g/t FY26 sustainability into FY27. [D002, p.3]
- Q9: Reconcile White Devil ~3Mt @ 3.8g/t (~350Koz) to 50→100Koz/yr ramp over 5 years. [D002, p.3]
- Q10 (remainder): Confirm Royal Sheba first production timing; not double-counted with BTRP. [D002, p.3; D003, p.6]
- Q14: Check FY27 MTR production split; H1 FY27 below nameplate, Q2–Q4 step-up to ~60Koz annualised. [D003, p.6]
- Q15: Check FY27 BTRP guidance; flotation benefit FY27 or FY28. [D003, p.6]
- Q17: Check Elikhulu FY27 guidance vs FY26 57,092oz sold; Winkelhaak feed contribution. [D003, p.6; D008.2, p.42]
- Q18: Check FY27 Tennant grade assumption and White Devil strip ratio/grade. [D003, p.6]
- Q21: Confirm Fairview 47,678oz vs table 47,677oz rounding. [D003, p.6–7]
- Q37: Confirm Tennant FY27 capex guidance; crusher/mill/filter complete or continuing. [D006.2, p.22; D006.6, p.29]
- Q45: Confirm FY26 Tennant full-year production/grade to anchor FY27 run-rate. [D006.2, p.23]
- Q46: Confirm July 2026 deliveries against contract liability 8,030 included in FY27 ounces/revenue, not double-counted. [D006.3, p.25; D006.10, p.35]
- Q48: Reconcile Australia revenue 132,804 to Tennant segment revenue in D006.2. [D006.3, p.25, fn 1]
- Q66 (remainder): Confirm FY27 tailings/stockpile feed assumption; FY26 tailings = 123,051oz of 272,373oz (45%). [D008.2, pp.42–43]
- Q70 (remainder): Confirm FY27 Tennant capex guidance; FY26 expansion capex 68.4. [D008.2, p.40; D008.3, p.44]
- Q71 (remainder): Confirm FY27 MTR and Elikhulu capex guidance; FY26 expansion capex 29.9 / 19.4. [D008.2, p.40; D008.3, p.44]
- Q97: Check D009 for any Emmerson/Tennant Creek ounces, exploration spend or royalty contribution in FY27 guidance; confirm not double-counted with Tennant. [D006.9, p.34]
- Q125 (remainder): Explain group AISC rise US$1,600→US$1,867/oz; confirm what US$2,598→US$3,487/oz refers to; FY27 outlook. [D008.2, pp.42–43]
- Q133: Confirm whether AISC is built on cash-cost or total-cost basis; locate US$60,288k production D&A and where it sits. [D008.2, p.40]
- Q134: Reconcile gold sold vs produced by mine (Elikhulu 57,092 vs 56,475; MTR 53,133 vs 51,927). [D008.2, p.42]
- Q135: Confirm correct FY25→FY26 group AISC series; identify 2,598/3,487 metric. [D008.2, pp.42–43]
- Q136: Extract FY27 capex guidance by mine; confirm Tennant build completion and step-down from FY26 195.0/202.2. [D008.2, p.40; D008.3, p.44]
- Q137: Confirm FY27 budget FX rates; quantify FX sensitivity on US$ AISC. [D008.2, pp.42–43]
- Q138: Confirm FY26 Tennant AIC US$4,339/oz is first meaningful full-year figure; extract FY27 guidance. [D008.2, p.43]
- Q139: Confirm FY27 tailings vs underground mix guidance. [D008.2, pp.42–43]
- Q144: Confirm FY27 by-product credit assumption (FY26 4.1). [D008.2, pp.40–41]
- Q154: Extract FY27 group and by-mine capex guidance; confirm Tennant step-down from 68.4 and MTR from 29.9 (FY26 total 224.0; sustaining 21.8, expansion 202.2). [D008.3, p.44]
- Q127 (remainder): Confirm FY27 by-product credit assumption (FY26 4.1). [D008.2, pp.40–41]
- Q148: Confirm AIC expansion add-back = 202.2 − 7.2 = 195.0 exactly; confirm no other non-gold capex inside 195.0. [D008.2, p.40; D008.3, p.44]
- Q126 (remainder): Confirm non-gold capital excluded from AISC; AIC adds expansion capex 195.0; check if any non-gold capex sits inside. [D008.2, p.40; D008.3, p.44]
```

### 5. Baseline Forecast Inputs Captured Here

| Metric | FY26 | FY25 | Source |
| --- | --- | --- | --- |
| Adjusted EBITDA — by operation (group) | 663.1 | 245.8 | D008.4, p. 45 |
| Adjusted EBITDA — LFCF starting point | 609.4 | 226.6 | D008.4, p. 46 |
| Net income before finance costs — by operation | 602.2 | 239.8 | D008.4, p. 45 |
| Mining D&A — by operation | 60.1 | 32.1 | D008.4, p. 45 |
| Barberton Mines Adjusted EBITDA | 142.5 | 71.1 | D008.4, p. 45 |
| Evander Mines Adjusted EBITDA | 120.9 | 16.2 | D008.4, p. 45 |
| BTRP Adjusted EBITDA | 29.4 | 22.8 | D008.4, p. 45 |
| Elikhulu Adjusted EBITDA | 171.4 | 81.5 | D008.4, p. 45 |
| MTR Adjusted EBITDA | 155.9 | 51.8 | D008.4, p. 45 |
| Tennant Adjusted EBITDA | 43.0 | 2.4 | D008.4, p. 45 |
| Tennant bargain gain (FY25 add-back) | – | (28.0) | D008.4, p. 45 |
| Finance costs paid | (15.0) | (21.4) | D008.4, p. 46 |
| Income tax paid | (74.1) | (20.1) | D008.4, p. 46 |
| Net working capital movement | 46.6 | (2.0) | D008.4, p. 46 |
| Capital expenditure | (215.8) | (157.9) | D008.4, p. 46 |
| Proceeds from borrowings | – | 139.5 | D008.4, p. 46 |
| Repayment of borrowings | (149.3) | (117.2) | D008.4, p. 46 |
| Levered free cash flow | 201.8 | 47.5 | D008.4, p. 46 |
| Shares in issue (m) | 2,333.7 | 2,335.7 | D008.4, p. 46 |
| Treasury shares (m) | (306.4) | (306.4) | D008.4, p. 46 |
| Total shares for per-share metrics (m) | 2,027.3 | 2,029.3 | D008.4, p. 46 |
| Attributable cash flow per share (US cents) | 9.95 | 2.34 | D008.4, p. 46 |
| Last traded price (US cents) | 125.09 | 62.48 | D008.4, p. 46 |
| Cash flow yield per share | 7.96% | 3.75% | D008.4, p. 46 |
| US$/ZAR closing rate (30 June) | 16.46 | 17.75 | D008.4, p. 46, fn 1 |
| Total equity | 1,036.0 | 546.7 | D008.4, p. 46 |
| NAV per share (US cents) | 51.10 | 26.94 | D008.4, p. 46 |
| Net income before finance costs (ROCE numerator) | 545.8 | 215.9 | D008.4, p. 47 |
| Average equity | 791.3 | 455.4 | D008.4, p. 47 |
| Average borrowings | 120.8 | 158.9 | D008.4, p. 47 |
| ROCE | 59.8% | 35.1% | D008.4, p. 47 |
| EPS (ZA cents) | 298.12 | 131.91 | D008.4, p. 47 |
| EPS (pence) | 13.36 | 5.63 | D008.4, p. 47 |
| DPS (ZA cents) | 77.00 | 37.00 | D008.4, p. 47 |
| DPS (pence) | 3.53 | 1.52 | D008.4, p. 47 |
| Maiden interim DPS (ZA cents) | 12.00 | – | D008.4, p. 47, fn 1 |

### 6. Next Section to Capture

**`D006.2` (Note 3 Segment Analysis, pp. 20–24)** — resolves the highest-priority open items: **Q157** (663.1 vs 609.4 EBITDA bridge), **Q158** (three conflicting FY25 Adjusted EBITDA figures), **Q159** (impairment location/quantum), **Q162** (Tennant FY25 base effect), and **Q164/Q166** (margin and ROCE numerator reconciliation). If D006.2 is unavailable, **`D006.10` (Notes 19–21, p. 35–36)** is the next best for **Q160/Q161** (STI/gold trading/rehab FV treatment) and **Q121/Q123** (FCF and headline earnings reconciliations).