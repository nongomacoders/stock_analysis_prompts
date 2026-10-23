# Section 14: Financial notes — Notes 22,23,24

> **Package**: `section-3410c2d10e264a6c817cd9f3e454eacf`  
> **Report**: `Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf` (annual_report)  
> **Model**: `deepseek/deepseek-v4.1-flash-1017`  
> **Execution Time**: 45.44s  
> **Cost**: $0.0029  
> **Tokens**: 14,558 total (8,176 prompt / 6,382 completion)  

### 1. Answers to Stored Questions for This Section

- **Q104 & Q85 (net finance cost reconciliation)**: **Not resolved here.** D006.11 contains no finance cost/income figures. The 4,652 gap (Note 5 net 12,612 vs D006.8 gross 12,666) remains open — carry forward to D008/D005.
- **Q88 & Q106 (rehabilitation provision / DMPR guarantee 39,566)**: **Not resolved here.** No rehabilitation provision balance or DMPR guarantee figure appears in D006.11. Carry forward.
- **Q24 (remainder) — reciprocal dividend**: **Partially resolved.** D006.11 confirms the "Intra-Group PAR Gold reciprocal dividend" is referenced to the Statement of Changes in Equity `[D006.11, p.36]` — i.e., it is an intra-group/treasury item, not an external cash dividend. The 8,847 figure and treasury-share mechanics still require D005.1 confirmation. Remainder stays open.
- **Q40 / Q72 / Q96 (solar disposal & electricity)**: **Partially resolved.** D006.11 confirms the Evander Solar Solutions → Evander Mines/Elikhulu electricity charge is an **intra-group related-party transaction** referenced to Note 3 segment analysis `[D006.11, p.36]`. This means the solar electricity cost is internal and will be eliminated on consolidation — relevant to how the "electricity cost step-up post-disposal" should be modelled (only external PPA cost matters). Disposal timing/gain still open.
- **Q107 (NOA Group PPA)**: **Not resolved here** — no PPA terms in D006.11. Carry forward.
- **Q93 / Q77 (Emmerson 102,641,421 shares)**: **Resolved (confirmation).** D006.11 Note 24 confirms 102,641,421 new Pan African shares (ASX CDIs) issued **1 July 2026** to Emmerson shareholders, i.e., post-year-end, excluded from 30 June 2026 issued count and included in FY27 weighted average from 1 July 2026 `[D006.11, p.36]`. This corroborates the D006.9 treatment; EPS/DPS denominator mechanics still to be checked in D005.1.
- **Q95 (Emmerson transaction costs)**: **Not resolved here** — no cost figure in D006.11. Carry forward.

*(All other stored questions relate to sections not in this capture and are carried forward in Section 4.)*

### 2. Footnote & Qualification Deep-Dive

- **No footnote markers (`[^1]`, `*`) are present in this section.** The section is narrative notes only; there are no table footnotes to unpack. No missing-footnote flags required.
- **Note 22 — related party scope qualification**: The note states "No further material related party transactions occurred… during the current or previous reporting period" `[D006.11, p.36]`. This is a **completeness assertion** that must be tested: it implies the only related-party flows are (i) intra-group interest/management fees, (ii) intra-group loans (no fixed terms, repayable on demand, treasury interest), (iii) PAR Gold reciprocal dividend, and (iv) Evander Solar electricity charge. Any external related-party revenue/cost (e.g., directors, BEE partners, community trusts) is asserted nil — verify against Note 3 segment analysis and the APM section.
- **Note 23 — litigation qualifications**: Three matters (Evander/MPC CMA arbitration; Barberton Nature Reserve NPA charges; Barberton land claim). All are qualified "likelihood of any outflow… is remote" `[D006.11, p.36]`. Forecast implication: **no provision should be modelled**, but the NPA response deadline of **29 September 2026** falls in FY27 H1 — a contingent-risk watch item, not a P&L item. The land claim is asserted not to affect the mining right — verify no impairment trigger on Barberton CGU (links Q64).
- **Note 24 — post-balance-sheet event**: Confirms the Emmerson share issuance is a **non-adjusting post-year-end event** (1 July 2026). Forecast implication: FY26 share count/EPS unaffected; FY27 weighted average includes the 102.6m shares for the full year. No cash outflow (share-for-share).

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| Q113 | High | D006.2 (Note 3 Segment Analysis) | Note 22 asserts intra-group interest, management fees and Evander Solar electricity charge are the only related-party flows, all referenced to Note 3 `[D006.11, p.36]` | In Note 3, confirm the intra-group management fee and electricity charge amounts and that they eliminate on consolidation; confirm no external related-party revenue/cost lines | Prevents double-counting internal electricity/management costs in group cost base and AISC |
| Q114 | Medium | D008 (APM) | Evander Solar electricity is intra-group `[D006.11, p.36]`; Q40/Q72 expect a post-disposal electricity step-up | Confirm whether AISC/electricity cost reflects external PPA (NOA) only, and quantify the external electricity cost that survives consolidation post solar disposal | Determines true FY27 unit cost step-up vs internal transfer |
| Q115 | Medium | D005.1 / D006.7 | PAR Gold reciprocal dividend referenced to Statement of Changes in Equity `[D006.11, p.36]` | Confirm the 8,847 reciprocal dividend is intra-group (eliminated) and not an external cash outflow; confirm treasury-share mechanics | Avoids modelling a phantom cash dividend; affects distributable reserves and dividend policy |
| Q116 | Low | D008 / D003 | Litigation: NPA response due 29 Sept 2026; land claim; CMA arbitration all "remote" `[D006.11, p.36]` | Confirm no provision/impairment recognised for Barberton CGU or Evander; check for any disclosed contingent liability quantum | Confirms no FY27 P&L hit; watch for Barberton CGU impairment trigger (links Q64) |
| Q117 | Low | D005.1 | Note 24 confirms 102,641,421 Emmerson shares issued 1 July 2026 `[D006.11, p.36]` | Confirm FY27 weighted average share count and EPS/DPS denominators include these shares from 1 July 2026 | EPS/DPS forecast accuracy (links Q77, Q93) |

### 4. Updated Open Questions Ledger (Copy to App)

```markdown
# OPEN QUESTIONS LEDGER — after D006.11 (Notes 22,23,24)

## Pending: D005.1 (Primary financial statements)
- Q52: Extract pre-tax profit from P&L; compute FY26/FY25 ETR; confirm 33.2%/28.5%. [D006.4, p.25]
- Q24 (remainder): Confirm reciprocal dividend (8,847) cash round-trip on 13.1% treasury; net vs gross; FY27 dividend policy. Note 22 confirms it is an intra-group PAR Gold item referenced to SOCIE. [D005.1, p.18–19; D006.7, p.30; D006.11, p.36]
- Q25 (remainder): Extract FY26 SBP P&L charge and FY27 expected charge; explain "Other expenses" 85,958 vs 36,484. [D005.1, p.17–18; D006.2, p.21,23]
- Q31 (remainder): Reconcile cash+STI US$246.2m and debt facilities US$78.9m to cash flow statement and Emmerson/equity issuance. Note 16 carrying value US$51,535k vs facilities US$220,550k — US$78.9m definition unresolved. [D006.1, p.19; D006.8, p.31,33; D006.10, p.35]
- Q44: Reconcile segment net assets 1,017,559 + goodwill 18,438 = 1,035,997 to group total equity. [D006.2, p.22]
- Q67: Reconcile "Inventory recognised in cost of production" 57,468 vs 27,358 (+US$30,110k) to cost of sales in P&L and production volumes. Note 19 shows inventory decrease 17,411 (cash flow). [D006.6, p.29; D006.10, p.35]
- Q69: Check cash flow statement for VAT/GST receivable 18,107 timing and expected FY27 unwind. Note 19 shows other receivables increase 21,206. [D006.6, p.29; D006.10, p.35]
- Q77: Confirm FY27 weighted average share count including 102,641,421 Emmerson shares issued 1 July 2026 (confirmed Note 24); check EPS and DPS calculations. [D006.7, p.30; D006.9, p.34; D006.11, p.36]
- Q78: Confirm share buy-back cash cost (~US$1,322k) in cash flow statement financing activities; check if further buy-backs planned FY27. [D006.7, p.30]
- Q79: Confirm working capital movement for other payables +US$29,480k in cash flow statement; Note 19 shows trade and other payables increase 50,354 — reconcile the 20,874 difference. [D006.7, p.30; D006.10, p.35]
- Q80: Confirm VAT payable US$5,836k payment timing in cash flow statement; check jurisdiction (Australia vs South Africa). [D006.7, p.30]
- Q83 (remainder): Confirm treasury share treatment in EPS and dividend calculations; check if treasury shares will be cancelled or reissued. Note 15 confirms share premium cancelled but not treasury shares. [D006.7, p.30; D006.8, p.31]
- Q84: Check cash flow statement financing activities for total debt repayments US$149,311k; reconcile to net debt movement. Note 20.1 shows borrowings fell 189,977→51,535 (reduction 138,442). [D006.8, pp.31–32; D006.10, p.35]
- Q85: Check P&L net finance costs line; Note 19 shows finance costs 17,318 and finance income (4,706) = net 12,612, vs D006.8 gross 12,666 — reconcile 4,652 gap. [D006.8, pp.31–32; D006.10, p.35]
- Q90: Check Statement of Changes in Equity for US$10,877k share premium cancellation reclassification to retained earnings; confirm distributable reserves. [D006.8, p.31]
- Q92: Confirm 24,917,607 Tennant lender shares (issued FY25) are in FY26 weighted average share count; check EPS denominator. [D006.8, p.31, fn 1]
- Q93: Confirm 102,641,421 Emmerson shares excluded from 30 June 2026 issued count and included in FY27 weighted average from 1 July 2026 (confirmed Note 24); check EPS/DPS denominators and dividend implied share counts (links Q3, Q77). [D006.9, p.34; D006.11, p.36]
- Q98: Confirm reserve for shares to be issued US$148,218k presented in equity (Note 14) and reconciles to Statement of Changes in Equity; confirm no cash outflow. [D006.9, p.34]
- Q103: Identify missing ~43,831 FY26 adjustment line in Note 19 "Adjusted for" subtotal 143,482 (listed lines sum ~99,651; FY25 reconciles exactly to 30,079). [D006.10, p.35]
- Q109: Confirm FY27 payables unwind assumption; reconcile Note 19 trade and other payables increase 50,354 to D006.7 29,480. [D006.10, p.35; D006.7, p.30]
- Q117: Confirm FY27 weighted average share count and EPS/DPS denominators include 102,641,421 Emmerson shares from 1 July 2026. [D006.11, p.36]

## Pending: D008 (Alternative performance measures)
- Q2: Obtain AISC reconciliation (by operation and group); confirm vs guidance US$1,820–1,870/oz. [D002, p.3]
- Q11: Confirm renewable energy US$5.1m in FY26 base; water savings US$1.4m/yr incremental FY27+. [D002, p.2–3]
- Q20: Reconcile Elikhulu US$1,231/oz, MTR US$1,389/oz, BTRP US$1,564/oz to group AISC. [D003, p.6]
- Q34 (remainder): Confirm page 72 APM reconciliation; AISC/APM definitions tie to IFRS. [D006.1, p.19; D006.2, p.22,24]
- Q36: Confirm Adjusted EBITDA definition; restate FY25 (249,724 + 2,954 = 252,678). [D006.2, p.22,24]
- Q40: Confirm no FY27 solar segment; electricity cost step-up post-disposal; disposal gain/loss; solar capex 7,159 in FY26. Note 21 confirms solar plant still under construction at FY26. Note 22 confirms Evander Solar electricity is intra-group. [D006.2, p.20–21; D006.6, p.29; D006.10, p.36; D006.11, p.36]
- Q42: Confirm segment AISC/APMs before or after intra-group management fee allocation. [D006.2, p.21]
- Q47 (remainder): Check FY27 capex interest-capitalisation; FY27 finance cost run-rate. FY26 gross finance costs US$12,666k; term/Realside/NT/NAB settled, only RCF+DMTN remain. Need DMTN coupon rates. [D006.4, p.25; D006.8, pp.31–32]
- Q50: Confirm restricted cash 2,612 nature; finance income 60 FY26 vs nil FY25. Note 20.1 confirms 2,612 at amortised cost. [D006.10, p.35]
- Q57: Confirm ZAR/AUD FX rate FY26 close vs FY25; FY27 FX sensitivity on DTL. [D006.4, p.26]
- Q63: Confirm AISC uses production D&A US$60,288k (not total PPE depreciation US$61,733k); identify US$2,179k "other D&A". Note 19 shows total D&A 61,980. [D006.5, p.28; D006.10, p.35]
- Q64: Confirm no further FY27 impairment; check CGU headroom assumptions (incl. Barberton land claim — Note 23). [D006.5, p.28; D006.11, p.36]
- Q26 (remainder): FY27 expected effective tax rate — check D008/D009. [D006.1, p.19–20]
- Q32 (remainder): FY27 ETR from deferred tax note — rates given, no forward ETR. [D006.1, p.19–20]
- Q39 (remainder): FY27 ETR, mining tax vs corporate tax split. [D006.2, p.21,23]
- Q53: Confirm no remaining tax losses; model FY27 current tax at full statutory rates. [D006.4, p.26]
- Q58: Confirm why Barberton deferred tax rate stepped 24.00%→28.29%; FY27 stability. [D006.4, p.26]
- Q30: Confirm FY27 budget gold price deck (base US$4,600→US$4,900/oz; downside US$3,680/oz +10% production cut) and FX assumption; decide forecast deck. [D006.1, p.19]
- Q66: Confirm FY27 tailings/stockpile feed assumption; quantify tailings contribution to FY26 ounces (long-term inventory 25,698→11,911). [D006.6, p.29]
- Q68: Check cyanide cost per tonne and whether prepayments 15,914 unwind in FY27; working capital movement. [D006.6, p.29]
- Q70: Confirm FY27 Tennant capex guidance; crusher/mill/filter/White Devil completion (links Q37, Q60). [D006.6, p.29]
- Q71: Confirm FY27 MTR and Elikhulu capex guidance; MTR expansion completion (links Q14, Q17). [D006.6, p.29]
- Q72: Confirm solar projects status at FY26 year-end, disposal timing/gain, FY27 electricity cost step-up. Note 21 confirms plant under construction; Note 22 confirms intra-group electricity charge. [D006.6, p.29; D006.10, p.36; D006.11, p.36]
- Q75: Confirm nature/collectability of other receivables 7,828 (Evander/Barberton); loss allowance adequacy. [D006.6, p.29]
- Q81: Confirm whether STI FV gain US$1,142k is excluded from Adjusted EBITDA/AISC; confirm STI treatment in net debt calculation. Note 19 confirms gain added back. [D006.7, p.30; D006.10, p.35]
- Q86: Check D008/D003 for RCF renewal/refinancing plans before 30 June 2027 maturity; confirm FY27 liquidity headroom. [D006.8, p.31]
- Q87: Check D008 for quantified JIBAR→ZARONIA interest rate impact; confirm whether ZARONIA differs materially from JIBAR. [D006.8, pp.31–32]
- Q89: Check D008 net debt definition — are gold loan facility US$25,557k and gold trading facilities US$58,931k included in net debt or excluded as trading? Confirm gold borrowing volumes. [D006.8, p.33]
- Q94: Check Note 7 (PPE) for exploration asset carrying value US$142,244k at 30 June 2026; confirm FY27 depletion/amortisation or impairment treatment; confirm D008 AISC exclusion. [D006.9, p.34]
- Q95: Confirm Emmerson transaction costs US$11,879k capitalised (not in FY26 P&L/Adjusted EBITDA); check APM add-back/exclusion; confirm no FY27 opex double-count. [D006.9, p.34]
- Q96: Reconcile Note 18.2 "no disposals" against solar disposal expectation (Q40/Q72); confirm solar disposal timing/gain and FY27 electricity cost step-up. [D006.9, p.34]
- Q100: Confirm treatment of cash-settled SBP current portion US$43,969k in net debt/liquidity; confirm FY27 cash settlement (FY26 settlement 18,200). [D006.9, p.33; D006.10, p.35]
- Q101: Confirm whether SBP expense US$57,272k is excluded from Adjusted EBITDA/AISC; if not, quantify FY27 SBP at assumed share price. [D006.9, p.33; D006.10, p.35]
- Q102: Confirm PAR Gold G-share vesting/settlement (11,541,455, vest 30 June 2026) in FY27 cash flow; confirm I-share FY27 expense and cash vs equity settlement. [D006.9, p.34]
- Q105: Identify which projects the 309,076 board-approved commitments and 94,580 open orders relate to (Tennant, MTR, solar, Soweto); tie to FY27 capex guidance. [D006.10, p.36]
- Q107: Quantify PPA with NOA Group (3 July 2025, 10+5 years) cost commitment and expected start date; confirm FY27 electricity cost step-up and solar disposal timing/gain. [D006.10, p.36]
- Q108: Confirm STI 137,867 treatment in net debt and Adjusted EBITDA/AISC; confirm FY27 FV assumption. [D006.10, p.35–36]
- Q110: Confirm royalty cash outflow FY26 and FY27 forecast; confirm whether royalties are in AISC (Note 19 adds back 14,609; headline 712,119 is before royalties). [D006.10, p.35]
- Q112: Confirm FY27 rehab fund FV assumption and whether gain is excluded from Adjusted EBITDA. [D006.10, p.35–36]
- Q113: In Note 3, confirm intra-group management fee and Evander Solar electricity charge amounts eliminate on consolidation; confirm no external related-party revenue/cost lines. [D006.11, p.36]
- Q114: Confirm whether AISC/electricity cost reflects external PPA (NOA) only; quantify external electricity cost surviving consolidation post solar disposal. [D006.11, p.36]

## Pending: D009 (Group production summary)
- Q1: Confirm total group ounces, Sheba+Consort ounces and AISC; reconcile to ~US$3,500/oz tail. [D002, p.2–3]
- Q6: Confirm Elikhulu 56,475oz @ US$1,231/oz and MTR 51,927oz @ US$1,389/oz full-year; MTR expansion run-rate FY27. [D002, p.3]
- Q9: Reconcile White Devil ~3Mt @ 3.8g/t (~350Koz) to 50→100Koz/yr ramp over 5 years. [D002, p.3]
- Q5 (remainder): Confirm Tennant FY27 capex $; White Devil first blast date and grade ramp. [D002, p.3; D003, p.6]
- Q7 (remainder): Confirm Evander underground grade >11g/t FY26 sustainability into FY27. [D002, p.3]
- Q10 (remainder): Confirm Royal Sheba first production timing; not double-counted with BTRP. [D002, p.3; D003, p.6]
- Q14: Check FY27 MTR production split; H1 FY27 below nameplate, Q2–Q4 step-up to ~60Koz annualised. [D003, p.6]
- Q15: Check FY27 BTRP guidance; flotation benefit FY27 or FY28. [D003, p.6]
- Q17: Check Elikhulu FY27 guidance vs FY26 56,475oz; Winkelhaak feed contribution. [D003, p.6]
- Q18: Check FY27 Tennant grade assumption and White Devil strip ratio/grade. [D003, p.6]
- Q21: Confirm Fairview 47,678oz vs table 47,677oz rounding. [D003, p.6–7]
- Q37: Confirm Tennant FY27 capex guidance; crusher/mill/filter complete or continuing. [D006.2, p.22; D006.6, p.29]
- Q45: Confirm FY26 Tennant full-year production/grade to anchor FY27 run-rate. [D006.2, p.23]
- Q46: Confirm July 2026 deliveries against contract liability 8,030 included in FY27 ounces/revenue, not double-counted. Note 19 confirms advance consideration 8,030. [D006.3, p.25; D006.10, p.35]
- Q48: Reconcile Australia revenue 132,804 to Tennant segment revenue in D006.2. [D006.3, p.25, fn 1]
- Q65: Extract segment-level D&A from Note 3 to split Tennant/Emmerson vs SA. [D006.5, p.28]
- Q66: Confirm FY27 tailings/stockpile feed assumption; quantify tailings contribution to FY26 ounces. [D006.6, p.29]
- Q67: Reconcile inventory charged to production 57,468 to production volumes. [D006.6, p.29]
- Q70: Confirm FY27 Tennant capex guidance and completion status. [D006.6, p.29]
- Q71: Confirm FY27 MTR and Elikhulu capex guidance. [D006.6, p.29]
- Q97: Check D009 for any Emmerson/Tennant Creek ounces, exploration spend or royalty contribution in FY27 guidance; confirm not double-counted with Tennant. [D006.9, p.34]

## Pending: D002 / D003 (Highlights / CEO statement)
- Q3: Reconcile dividend implied share counts: 2,436m / 2,333m / 2,420m; issued/weighted count, Emmerson shares, treasury. [D002, p.2; D006.7, p.30; D006.9, p.34]
- Q4: Confirm FX rate/date for dividend US$ conversion (implied ~16.40–16.46 vs stated avg 16.90). [D002, p.2]
- Q8: Confirm Soweto Cluster DFS gold price assumption; FID timing Dec 2026; financing plan; capex post-FY27. [D002, p.3]
- Q12: Quantify SBP expense FY26 vs FY25 and FY27 assumption. [D002, p.3; D006.9, p.33]
- Q16: Locate Tennant FY27 capex $ for fixed crusher, secondary mill, belt filter; capitalised vs expensed. [D003, p.6]
- Q19: Extract total FY27 group capex guidance and Tennant-specific split (FY26 actual 223,995 captured). [D003, p.6; D006.6, p.29]
- Q115: Confirm 8,847 reciprocal dividend is intra-group (eliminated), not external cash outflow; confirm treasury-share mechanics. [D006.11, p.36]
- Q116: Confirm no provision/impairment for Barberton CGU or Evander litigation; check contingent liability quantum. [D006.11, p.36]
```

### 5. Baseline Forecast Inputs Captured Here

| Item | Value / Fact | Source |
| --- | --- | --- |
| Emmerson shares issued post-year-end | 102,641,421 new Pan African shares (ASX CDIs), issued 1 July 2026 | `[D006.11, p.36]` |
| Emmerson acquisition | 100% of issued shares in Emmerson, settled in shares (no cash) | `[D006.11, p.36]` |
| Related-party flows (only) | Intra-group interest/management fees; intra-group loans (no fixed terms, on-demand, treasury interest); PAR Gold reciprocal dividend; Evander Solar→Evander Mines electricity charge | `[D006.11, p.36]` |
| Litigation provisions | Nil — all three matters assessed "remote" likelihood of outflow | `[D006.11, p.36]` |
| NPA response deadline | 29 September 2026 (FY27 H1) | `[D006.11, p.36]` |
| Post-balance-sheet adjusting events | None other than Emmerson share issuance | `[D006.11, p.36]` |

### 6. Next Section to Capture

**`D008` (Alternative Performance Measures, pp. 38–47)** — resolves the highest-priority open items: Q2 (AISC reconciliation), Q113/Q114 (intra-group electricity elimination and external PPA cost), Q40/Q72/Q96 (solar disposal & electricity step-up), Q47/Q85/Q104 (finance cost run-rate), Q89 (net debt definition incl. gold facilities), Q101/Q108 (SBP/STI treatment in APMs), and Q110 (royalties in AISC).