# Section 17: Alternative performance measures — SUSTAINING CAPITAL,EXPANSION CAPITAL,NET (CASH)/DEBT

> **Package**: `section-240bad8eaec442808809d51a376d19f8`  
> **Report**: `Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf` (annual_report)  
> **Model**: `deepseek/deepseek-v4.1-flash-1017`  
> **Execution Time**: 85.47s  
> **Cost**: $0.0043  
> **Tokens**: 20,117 total (9,258 prompt / 10,859 completion)  

### 1. Answers to Stored Questions for This Section

**Q120 (net debt reconciliation — treatment of gold loan, gold trading, STI, cash-settled SBP, restricted cash, IFRS 16 leases)**
- **Status**: `Partially resolved (remainder stays open for D006.8 / D008.1)`
- **Answer & evidence**: The D008.3 net (cash)/debt reconciliation `[D008.3, physical PDF p. 44]` shows: Cash and cash equivalents (108.3); Short-term investments (137.9); Borrowings 51.5; Financial instrument liability – (FY25: 1.8); Lease liability 7.8 (FY25: 3.9); Financial liability 1.2 (FY25: 3.3); Facility arrangement fees – (FY25: 0.9); **Net (cash)/debt (185.7)** vs FY25 150.5. Critically, **no separate line for gold loan (25,557) or gold trading (58,931) appears** — these must therefore be embedded inside "Borrowings 51.5" or excluded entirely. This is a material tension: 25.557 + 58.931 = 84.488, which exceeds total borrowings of 51.5, so at least one of the two must be excluded from net debt (or netted elsewhere). **Cash-settled SBP (43,969) is NOT visible as a line** — it is not in net debt per this table. **Restricted cash (2,612) is not separately shown** — it is presumably inside the 108.3 cash figure (i.e., not deducted). STI (137.9) **is** netted in net debt. Remainder (which of gold loan / gold trading sits in Borrowings 51.5, and where SBP 43,969 sits) stays open for D006.8/D008.1.

**Q129 (which financial liabilities added to net debt — SBP? gold loan? trading?)**
- **Status**: `Partially resolved`
- **Answer & evidence**: Net debt adds: Borrowings 51.5, Lease liability 7.8, Financial liability 1.2 `[D008.3, p. 44]`. There is **no SBP line, no gold loan line, no gold trading line**. So on the face of this table, none of SBP/gold loan/gold trading is added as a separate financial liability. The "Financial liability 1.2" is small and unexplained — needs identification in D006.8/D008.1.

**Q130 ("cash and related hedges" meaning; whether STI netted in net debt)**
- **Status**: `Resolved (definition) / Partially resolved (hedge composition)`
- **Answer & evidence**: The definition states net debt = total borrowings from financial institutions (before IFRS 9 adjustments) **less cash and cash equivalents including derivatives entered into to protect against FX or commodity price fluctuations** `[D008.3, p. 44]`. STI (137.9) **is** netted (shown as a negative). The "derivatives" wording implies commodity/FX hedges are netted within cash — but the table shows no separate derivative asset line, so the hedge amount is not quantifiable here. Remainder (quantum of hedges netted) stays open.

**Q86 (RCF renewal/refinancing before 30 June 2027 maturity; FY27 liquidity headroom)**
- **Status**: `Partially resolved (context only)`
- **Answer & evidence**: Borrowings fell from 190.0 to 51.5 and net debt swung to net cash (185.7) `[D008.3, p. 44]`. This materially improves FY27 liquidity headroom, but the section does **not** state RCF maturity, renewal, or committed undrawn facilities. Remainder stays open for D006.8/D008.1.

**Q84 (total debt repayments 149,311 reconcile to net debt movement)**
- **Status**: `Partially resolved (arithmetic check)`
- **Answer & evidence**: Borrowings movement 190.0 → 51.5 = **repayment of 138.5** `[D008.3, p. 44]`. This is **not equal** to the stored 149,311 debt repayment figure — a gap of ~10.8 must be explained (FX translation on ZAR/AUD debt, IFRS 9 adjustments excluded per definition, or new drawdowns). Flag as verification item.

**Q50 (restricted cash 2,612 nature)**
- **Status**: `Unresolved — carried forward`
- **Answer & evidence**: Not separately disclosed in D008.3; presumably inside cash 108.3. No new evidence.

**Q100 (cash-settled SBP current portion 43,969 in net debt/liquidity)**
- **Status**: `Partially resolved (negative)`
- **Answer & evidence**: SBP 43,969 is **not** a line in net debt `[D008.3, p. 44]`. So it does not inflate net debt here; but it remains a FY27 cash obligation outside this metric. Remainder (FY27 cash settlement timing) stays open.

**Q105 / Q136 / Q19 / Q70 / Q71 (capex by mine; FY27 capex guidance; step-down from FY26 195.0)**
- **Status**: `Partially resolved (FY26 actuals confirmed; FY27 guidance absent)`
- **Answer & evidence**: D008.3 confirms FY26 **total capital 224.0** (FY25 167.9), split **sustaining 21.8** (FY25 11.7) and **expansion 202.2** (FY25 156.2) `[D008.3, p. 44]`. By mine FY26 expansion: Barberton Mines 27.5 (BTRP 2.2 + mining ops 25.3); Evander 69.2 (Elikhulu 19.4 + mining ops 49.8); MTR 29.9; Tennant 68.4; Solar 7.2. Note the stored "FY26 expansion capex 195.0" differs from the 202.2 here — a **7.2 gap equals the Solar projects line**, suggesting the AISC/AIC "expansion capex 195.0" **excludes solar**. Flag. FY27 capex guidance is **not** in this section — stays open for D003/D009.

**Q126 (non-gold capital excluded from AISC; AIC adds expansion capex 195.0; any non-gold capex inside)**
- **Status**: `Partially resolved`
- **Answer & evidence**: Total expansion 202.2 vs AIC-referenced 195.0 → difference 7.2 = Solar projects `[D008.3, p. 44]`. This supports the hypothesis that solar (non-gold) capex is excluded from the AIC expansion add-back. Corporate sustaining 1.8 and Agricultural ESG 0.1 are small. Remainder (confirm 195.0 = 202.2 − 7.2 exactly, and whether any other non-gold sits inside) stays open for D008.2 cross-check.

**Q63 / Q140 (production D&A 60,288 vs total PPE depreciation 61,733; AISC reconciliation shows no D&A line)**
- **Status**: `Unresolved — carried forward`
- **Answer & evidence**: D008.3 does not address D&A. No new evidence.

**Q143 / Q112 (rehab fund FV gain treatment in Adjusted EBITDA; accretion)**
- **Status**: `Unresolved — carried forward`
- **Answer & evidence**: Not addressed in D008.3.

**Q40 / Q72 (solar disposal; FY27 electricity step-up)**
- **Status**: `Partially resolved (capex only)`
- **Answer & evidence**: Solar projects capex FY26 7.2 (FY25 3.5) `[D008.3, p. 44]` — still being capitalised in FY26, consistent with disposal not yet complete at year-end. Disposal timing/gain and electricity step-up not addressed here — stays open.

**Q96 (Note 18.2 "no disposals" vs solar disposal expectation)**
- **Status**: `Unresolved — carried forward`
- **Answer & evidence**: D008.3 shows solar capex still flowing in FY26 but no disposal evidence. No resolution.

**Q31 (reconcile cash+STI 246.2 and debt facilities 78.9 to cash flow statement)**
- **Status**: `Partially resolved`
- **Answer & evidence**: Cash 108.3 + STI 137.9 = **246.2** ✓ matches stored figure `[D008.3, p. 44]`. Borrowings 51.5 + lease 7.8 + financial liability 1.2 = **60.5** gross debt (vs stored "debt facilities 78.9" — gap 18.4, likely undrawn facilities or a different definition). Flag for D006.8.

**Q137 (FY27 budget FX rates; FX sensitivity on US$ AISC)**
- **Status**: `Unresolved — carried forward`
- **Answer & evidence**: Not addressed in D008.3.

**Q57 (ZAR/AUD FX close vs average)**
- **Status**: `Unresolved — carried forward`
- **Answer & evidence**: Not addressed in D008.3.

*(All other stored questions relate to sections not covered by this page and are carried forward in Section 4.)*

---

### 2. Footnote & Qualification Deep-Dive

- **No footnote markers (`[^1]`, `*`) are present in the supplied D008.3 evidence** `[D008.3, p. 44]`. There is therefore no buried footnote commentary to unpack on this page. This is itself notable: the two most consequential definitional caveats are in **body text**, not footnotes:
  1. **Net debt definition** `[D008.3, p. 44]`: "total borrowings from financial institutions (**before IFRS 9 accounting adjustments**) less cash and cash equivalents (**including derivatives** entered into in connection with protection against, or benefit from, fluctuations in exchange rates or commodity prices)." — This is a **non-IFRS definition**: it excludes IFRS 9 adjustments (so the balance-sheet borrowings figure will differ from the 51.5 here) and it **nets commodity/FX hedges against cash**. Implication: the 108.3 "cash" is a net-of-hedge figure, and the true gross cash may be higher. Must verify against the statement of financial position (D005) and Note 8/9 (D006.6).
  2. **Net senior debt definition** `[D008.3, p. 44]`: "secured, interest-bearing debt provided by financial institutions, net of available cash." — Excludes leases (7.8) and financial liability (1.2), and excludes STI? No — STI (137.9) **is** netted in senior debt too (shown as negative), giving net senior debt **(194.7)** vs net debt (185.7). The 9.0 difference = lease 7.8 + financial liability 1.2. This confirms leases and the 1.2 financial liability are **excluded** from senior debt but **included** in net debt.
- **Table structural anomaly** `[D008.3, p. 44]`: The sustaining/expansion capital table has **misaligned columns** in the capture (e.g., "Mining operations 12.2 | 8.3 | 25.3 16.6" — the FY25/FY26 pairing is ambiguous). The **Group total row is internally consistent**: sustaining 21.8 (FY26) / 11.7 (FY25); expansion 202.2 (FY26) / 156.2 (FY25); total 224.0 (FY26) / 167.9 (FY25). Check: 21.8 + 202.2 = 224.0 ✓; 11.7 + 156.2 = 167.9 ✓. But the **by-mine rows do not visibly sum to the group total** in the captured layout — e.g., expansion by mine: 27.5 + 69.2 + 29.9 + 68.4 + 7.2 = 202.2 ✓ (this does reconcile). Sustaining by mine: 12.6 + 1.7 + 2.7 + 2.9 + 0.1 + 1.8 = 21.8 ✓. So the totals reconcile; the column misalignment is a capture artefact, not a data error. **However**, the "Mining operations" sub-rows (Barberton 12.2/8.3; Evander –/–; etc.) appear to be **sub-components** of the mine totals, not additive — verify in D008.2/D006.2.
- **Key hidden implication**: The **195.0 vs 202.2** expansion capex gap (7.2 = solar) is the single most forecast-relevant item on this page — it tells us the AIC/AISC expansion add-back **excludes solar**, so FY27 AIC will not carry solar capex. Must confirm in D008.2.

---

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| Q146 | High | D006.8 (Notes 15,16) / D008.1 | Net debt table shows Borrowings 51.5 but **no gold loan (25,557) or gold trading (58,931) line**; 25.557+58.931=84.488 > 51.5 `[D008.3, p. 44]` | Identify whether gold loan and/or gold trading sit inside "Borrowings 51.5", are netted in cash, or are excluded. Reconcile to Note 15/16 borrowings. | Determines true gross debt and FY27 interest/repayment forecast. |
| Q147 | High | D006.8 / D008.1 | Borrowings movement 190.0→51.5 = 138.5 repayment, but stored debt repayments = 149,311; gap ~10.8 `[D008.3, p. 44]` | Reconcile 138.5 to cash flow financing repayments 149.3; explain FX translation / IFRS 9 / new drawdowns. | Validates debt schedule for FY27 net finance cost and net debt roll-forward. |
| Q148 | High | D008.2 (All-in Costs) | Expansion capex 202.2 (D008.3) vs AIC-referenced 195.0; gap 7.2 = Solar projects `[D008.3, p. 44]` | Confirm AIC expansion add-back = 202.2 − 7.2 = 195.0 exactly; confirm no other non-gold capex inside 195.0. | Sets FY27 AIC expansion component and confirms solar exclusion. |
| Q149 | High | D005 (Primary statements) / D006.8 | Net debt definition excludes IFRS 9 adjustments and nets FX/commodity derivatives against cash `[D008.3, p. 44]` | Tie 51.5 borrowings and 108.3 cash to statement of financial position; quantify IFRS 9 adjustment and hedge asset netted. | Gross vs net debt affects covenant and liquidity forecast. |
| Q150 | Medium | D006.8 / D008.1 | "Financial liability 1.2" unexplained; lease liability 7.8 `[D008.3, p. 44]` | Identify the 1.2 financial liability (SBP? other?); confirm lease 7.8 = IFRS 16 and FY27 lease payments. | Small but affects net debt definition and FY27 cash lease outflow. |
| Q151 | Medium | D006.8 / D008.1 | Net senior debt (194.7) vs net debt (185.7); difference 9.0 = lease 7.8 + financial liability 1.2 `[D008.3, p. 44]` | Confirm senior debt excludes leases and the 1.2 liability; confirm STI netted in both. | Clarifies covenant metric (senior debt) vs reported net debt. |
| Q152 | Medium | D006.8 / D008.1 | Cash-settled SBP 43,969 **not** in net debt `[D008.3, p. 44]` | Confirm SBP 43,969 sits in current liabilities (not debt); confirm FY27 cash settlement timing. | FY27 cash outflow not captured in net debt. |
| Q153 | Medium | D006.8 / D008.1 | Restricted cash 2,612 not separately shown; presumably inside 108.3 `[D008.3, p. 44]` | Confirm restricted cash 2,612 is inside cash 108.3 and not "available" for senior debt netting. | Affects true available liquidity. |
| Q154 | Medium | D003 / D009 | FY27 capex guidance absent from D008.3; FY26 total 224.0 (sustaining 21.8, expansion 202.2) `[D008.3, p. 44]` | Extract FY27 group and by-mine capex guidance; confirm Tennant step-down from 68.4 and MTR from 29.9. | Core FY27 FCF driver. |
| Q155 | Low | D006.2 (Segment) | By-mine "Mining operations" sub-rows (Barberton 12.2/8.3; Evander –/–) appear non-additive `[D008.3, p. 44]` | Confirm sub-row structure in segment note; ensure no double-count with mine totals. | Avoids capex double-count in model. |
| Q156 | Low | D006.6 (Notes 8,9,10,11) | Solar capex 7.2 in FY26 still flowing; disposal not evidenced `[D008.3, p. 44]` | Confirm solar assets still on balance sheet at 30 June 2026; disposal timing/gain; FY27 electricity step-up. | FY27 electricity cost and one-off disposal gain. |

---

### 4. Updated Open Questions Ledger (Copy to App)

```markdown
# OPEN QUESTIONS LEDGER — after D008.3 (Sustaining/Expansion Capital, Net (Cash)/Debt, p. 44)

## Pending: D009 (Group production summary)
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
- Q65: Extract segment-level D&A from Note 3 to split Tennant/Emmerson vs SA. [D006.5, p.28]
- Q66 (remainder): Confirm FY27 tailings/stockpile feed assumption; FY26 tailings = 123,051oz of 272,373oz (45%). [D008.2, pp.42–43]
- Q67: Reconcile inventory charged to production 57,468 to production volumes. [D006.6, p.29]
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

## Pending: D005.1 (Primary financial statements)
- Q24 (remainder): Confirm reciprocal dividend (8,847) cash round-trip on 13.1% treasury; net vs gross; FY27 dividend policy. [D005.1, p.18–19; D006.7, p.30; D006.11, p.36]
- Q25 (remainder): Extract FY26 SBP P&L charge and FY27 expected charge; explain "Other expenses" 85,958 vs 36,484. [D005.1, p.17–18; D006.2, p.21,23]
- Q31 (remainder): Reconcile cash+STI US$246.2m (confirmed 108.3+137.9) and debt facilities US$78.9m (vs gross debt 60.5 here) to cash flow statement and Emmerson/equity issuance. [D006.1, p.19; D006.8, p.31,33; D006.10, p.35; D008.3, p.44]
- Q34 (remainder): Confirm APM reconciliation ties to IFRS — AISC starts from IFRS cost of production 435.7; tie to P&L cost of sales. [D008.2, p.40]
- Q44: Reconcile segment net assets 1,017,559 + goodwill 18,438 = 1,035,997 to group total equity. [D006.2, p.22]
- Q52: Extract pre-tax profit from P&L; compute FY26/FY25 ETR; confirm 33.2%/28.5%. [D006.4, p.25]
- Q67: Reconcile "Inventory recognised in cost of production" 57,468 vs 27,358 (+US$30,110k) to cost of sales in P&L and production volumes. [D006.6, p.29; D006.10, p.35]
- Q69: Check cash flow statement for VAT/GST receivable 18,107 timing and expected FY27 unwind. [D006.6, p.29; D006.10, p.35]
- Q77: Confirm FY27 weighted average share count including 102,641,421 Emmerson shares issued 1 July 2026; check EPS and DPS calculations. [D006.7, p.30; D006.9, p.34; D006.11, p.36]
- Q78: Confirm share buy-back cash cost (~US$1,322k) in cash flow statement financing activities; further buy-backs FY27. [D006.7, p.30]
- Q79: Confirm working capital movement for other payables +US$29,480k in cash flow statement; reconcile to Note 19 trade and other payables increase 50,354. [D006.7, p.30; D006.10, p.35]
- Q80: Confirm VAT payable US$5,836k payment timing in cash flow statement; jurisdiction. [D006.7, p.30]
- Q83 (remainder): Confirm treasury share treatment in EPS and dividend calculations; cancellation/reissue. [D006.7, p.30; D006.8, p.31]
- Q84 (remainder): Check cash flow statement financing activities for total debt repayments US$149,311k; reconcile to net debt movement (borrowings 190.0→51.5 = 138.5; gap ~10.8). [D006.8, pp.31–32; D006.10, p.35; D008.3, p.44]
- Q85: Check P&L net finance costs line; reconcile Note 19 finance costs 17,318 and income (4,706) = net 12,612 vs D006.8 gross 12,666 (4,652 gap). [D006.8, pp.31–32; D006.10, p.35]
- Q90: Check SOCIE for US$10,877k share premium cancellation reclassification to retained earnings; distributable reserves. [D006.8, p.31]
- Q92: Confirm 24,917,607 Tennant lender shares (issued FY25) in FY26 weighted average share count; EPS denominator. [D006.8, p.31, fn 1]
- Q93: Confirm 102,641,421 Emmerson shares excluded from 30 June 2026 issued count and included in FY27 weighted average from 1 July 2026; EPS/DPS denominators. [D006.9, p.34; D006.11, p.36]
- Q98: Confirm reserve for shares to be issued US$148,218k presented in equity (Note 14) and reconciles to SOCIE; no cash outflow. [D006.9, p.34]
- Q103: Identify missing ~43,831 FY26 adjustment line in Note 19 "Adjusted for" subtotal 143,482. [D006.10, p.35]
- Q109: Confirm FY27 payables unwind assumption; reconcile Note 19 trade and other payables increase 50,354 to D006.7 29,480. [D006.10, p.35; D006.7, p.30]
- Q117: Confirm FY27 weighted average share count and EPS/DPS denominators include 102,641,421 Emmerson shares from 1 July 2026. [D006.11, p.36]
- Q149: Tie 51.5 borrowings and 108.3 cash to statement of financial position; quantify IFRS 9 adjustment and hedge asset netted in net debt definition. [D008.3, p.44; D005, p.17]

## Pending: D002 / D003 (Highlights / CEO statement)
- Q3: Reconcile dividend implied share counts: 2,436m / 2,333m / 2,420m; issued/weighted count, Emmerson shares, treasury. [D002, p.2; D006.7, p.30; D006.9, p.34]
- Q4: Confirm FX rate/date for dividend US$ conversion (implied ~16.40–16.46 vs stated avg 16.90). [D002, p.2; D008.2, p.42]
- Q8: Confirm Soweto Cluster DFS gold price assumption; FID timing Dec 2026; financing plan; capex post-FY27. [D002, p.3]
- Q11: Confirm renewable energy US$5.1m in FY26 base; water savings US$1.4m/yr incremental FY27+. [D002, p.2–3]
- Q12: Quantify SBP expense FY26 vs FY25 and FY27 assumption. [D002, p.3; D006.9, p.33]
- Q16: Locate Tennant FY27 capex $ for fixed crusher, secondary mill, belt filter; capitalised vs expensed. [D003, p.6]
- Q19: Extract total FY27 group capex guidance and Tennant-specific split (FY26 actual 224.0 total / 202.2 expansion captured; APM expansion capex 195.0). [D003, p.6; D006.6, p.29; D008.2, p.40; D008.3, p.44]
- Q115: Confirm 8,847 reciprocal dividend is intra-group (eliminated), not external cash outflow; treasury-share mechanics. [D006.11, p.36]
- Q116: Confirm no provision/impairment for Barberton CGU or Evander litigation; contingent liability quantum. [D006.11, p.36]

## Pending: D006 (Financial notes — various)
- Q26 (remainder): FY27 expected effective tax rate — check D008/D009. [D006.1, p.19–20]
- Q32 (remainder): FY27 ETR from deferred tax note. [D006.1, p.19–20]
- Q39 (remainder): FY27 ETR, mining tax vs corporate tax split. [D006.2, p.21,23]
- Q40: Confirm no FY27 solar segment; electricity cost step-up post-disposal; disposal gain/loss; solar capex 7,159/7.2 in FY26. [D006.2, p.20–21; D006.6, p.29; D006.10, p.36; D006.11, p.36; D008.3, p.44]
- Q42: Confirm segment AISC/APMs before or after intra-group management fee allocation. [D006.2, p.21]
- Q47 (remainder): Check FY27 capex interest-capitalisation; FY27 finance cost run-rate; DMTN coupon rates. [D006.4, p.25; D006.8, pp.31–32]
- Q50 (remainder): Confirm restricted cash 2,612 nature; finance income 60 FY26 vs nil FY25; confirm inside cash 108.3. [D006.10, p.35; D008.1, p.39; D008.3, p.44]
- Q53: Confirm no remaining tax losses; model FY27 current tax at full statutory rates. [D006.4, p.26]
- Q57 (remainder): Confirm ZAR/AUD FX rate FY26 close vs FY25; FY27 FX sensitivity on DTL; averages 16.90/0.68 captured. [D006.4, p.26; D008.2, pp.42–43]
- Q58: Confirm Barberton deferred tax rate step 24.00%→28.29%; FY27 stability. [D006.4, p.26]
- Q63 (remainder): Confirm AISC uses production D&A US$60,288k (not total PPE depreciation US$61,733k); identify US$2,179k "other D&A"; AISC reconciliation shows NO D&A line — resolve. [D006.5, p.28; D006.10, p.35; D008.2, p.40]
- Q64 (remainder): Confirm no further FY27 impairment; CGU headroom (Barberton land claim — Note 23). [D006.5, p.28; D006.11, p.36; D008.1, p.38]
- Q68: Check cyanide cost per tonne and prepayments 15,914 unwind in FY27; working capital movement. [D006.6, p.29]
- Q72: Confirm solar projects status at FY26 year-end, disposal timing/gain, FY27 electricity step-up. [D006.6, p.29; D006.10, p.36; D006.11, p.36]
- Q75: Confirm nature/collectability of other receivables 7,828 (Evander/Barberton); loss allowance adequacy. [D006.6, p.29]
- Q113: Confirm intra-group management fee and Evander Solar electricity charge eliminate on consolidation. [D006.11, p.36]
- Q140: Locate production D&A in Note 3/Note 7; confirm whether inside cost of production 435.7 or excluded from AISC. [D008.2, p.40]
- Q141: Map 309,076/94,580 commitments to specific projects (Tennant crusher/mill/filter, MTR expansion, White Devil) and FY27 timing. [D008.2, p.40]
- Q142: Confirm no FY27 voluntary severance / restructuring cost expected; check "Other expenses". [D008.2, pp.40–41]
- Q143: Confirm rehab fund FV gain/loss treatment in Adjusted EBITDA; accretion stays negative in FY27. [D008.2, pp.40–41]
- Q145: Confirm driver of corporate G&A step-up 18.7→34.9 and FY27 run-rate. [D008.2, pp.40–41]
- Q146: Identify whether gold loan (25,557) and/or gold trading (58,931) sit inside "Borrowings 51.5", are netted in cash, or are excluded; reconcile to Note 15/16 borrowings. [D008.3, p.44; D006.8, p.31–33]
- Q147: Reconcile borrowings movement 138.5 to cash flow financing repayments 149.3; explain FX translation / IFRS 9 / new drawdowns. [D008.3, p.44; D006.8, pp.31–32; D006.10, p.35]
- Q150: Identify the 1.2 financial liability (SBP? other?); confirm lease 7.8 = IFRS 16 and FY27 lease payments. [D008.3, p.44]
- Q151: Confirm senior debt excludes leases and the 1.2 liability; confirm STI netted in both net debt and net senior debt. [D008.3, p.44]
- Q152: Confirm SBP 43,969 sits in current liabilities (not debt); confirm FY27 cash settlement timing. [D008.3, p.44; D006.9, p.33; D006.10, p.35]
- Q153: Confirm restricted cash 2,612 is inside cash 108.3 and not "available" for senior debt netting. [D008.3, p.44; D006.10, p.35]
- Q155: Confirm by-mine "Mining operations" sub-rows (Barberton 12.2/8.3; Evander –/–) are non-additive to mine totals; avoid double-count. [D008.3, p.44; D006.2, p.22]
- Q156: Confirm solar assets still on balance sheet at 30 June 2026; disposal timing/gain; FY27 electricity step-up. [D008.3, p.44; D006.6, p.29; D006.10, p.36]

## Pending: D008.1 / D008.2 (APMs — carried forward)
- Q89 (remainder): Confirm gold loan 25,557 and gold trading 58,931 included/excluded from net debt. [D006.8, p.33; D008.1, p.39; D008.3, p.44]
- Q119: Locate Adjusted EBITDA reconciliation; confirm SBP NOT added back, STI FV gain added back, impairment quantum, FY25 restated 252,678. [D008.1, p.38]
- Q120 (remainder): Confirm treatment of gold loan 25,557, gold trading 58,931, STI 137,867, cash-settled SBP 43,969, restricted cash 2,612, IFRS 16 leases in net debt. [D008.1, p.39; D008.3, p.44]
- Q121: Locate FCF reconciliation; identify "permitted indebtedness"-funded capex and IAS 7 non-cash adjustments; reconcile to cash flow statement. [D008.1, p.39]
- Q122: Locate LFCF reconciliation; confirm RCF repayment (30 June 2027 maturity) modelled; tie to net debt movement. [D008.1, p.39]
- Q123: Locate headline earnings reconciliation; confirm disposal/impairment/tax adjustments and EPS denominator. [D008.1, p.39]
- Q128: Confirm STI (137,867) and gold trading (58,931) classified as "normal course" derivatives for Adjusted EBITDA add-back. [D008.1, p.38]
- Q129 (remainder): Confirm which financial liabilities added to net debt (SBP? gold loan? trading?). [D008.1, p.39; D008.3, p.44]
- Q130 (remainder): Confirm "cash and related hedges" meaning; whether STI netted in net debt. [D008.1, p.39; D008.3, p.44]
- Q131: Confirm rehab fund FV gain treatment in Adjusted EBITDA. [D008.1, p.38]
- Q132: Identify IAS 7 non-cash items adjusted in FCF; confirm SBP treatment in FCF. [D008.1, p.39]
- Q148: Confirm AIC expansion add-back = 202.2 − 7.2 = 195.0 exactly; confirm no other non-gold capex inside 195.0. [D008.2, p.40; D008.3, p.44]
- Q126 (remainder): Confirm non-gold capital excluded from AISC; AIC adds expansion capex 195.0; check if any non-gold capex sits inside. [D008.2, p.40; D008.3, p.44]

## Pending: D006.2 / D006.8 / D006.9 (specific)
- Q36 (remainder): Confirm FY25 restated Adjusted EBITDA 252,678 in reconciliation table. [D006.2, p.22,24; D008.1, p.38]
- Q81 (remainder): Confirm STI FV gain US$1,142k excluded from Adjusted EBITDA/AISC; confirm STI treatment in net debt. [D006.7, p.30; D006.10, p.35; D008.1, p.38–39]
- Q86 (remainder): Confirm RCF renewal/refinancing plans before 30 June 2027 maturity; FY27 liquidity headroom (net cash 185.7 improves headroom). [D006.8, p.31; D008.1, p.39; D008.3, p.44]
- Q87: Quantify JIBAR→ZARONIA interest rate impact; confirm ZARONIA vs JIBAR. [D006.8, pp.31–32; D008.1, p.39]
- Q94 (remainder): Confirm exploration asset carrying value US$142,244k; FY27 depletion/impairment; AISC exclusion confirmed (no exploration line in AISC). [D006.9, p.34; D008.2, p.40]
- Q95 (remainder): Confirm Emmerson transaction costs US$11,879k capitalised (not in P&L/Adjusted EBITDA); no APM add-back confirmed. [D006.9, p.34; D008.2, p.40]
- Q96 (remainder): Reconcile Note 18.2 "no disposals" against solar disposal expectation; confirm timing/gain and FY27 electricity step-up. [D006.9, p.34; D008.1, p.39; D008.3, p.44]
- Q100 (remainder): Confirm cash-settled SBP current portion US$43,969k in net debt/liquidity; FY27 cash settlement. [D006.9, p.33; D006.10, p.35; D008.1, p.39; D008.3, p.44]
- Q102: Confirm PAR Gold G-share vesting/settlement (11,541,455, vest 30 June 2026) in FY27 cash flow; I-share FY27 expense. [D006.9, p.34; D008.1, p.38]
- Q105 (remainder): Identify projects for 309,076 board-approved commitments and 94,580 open orders; tie to FY27 capex (FY26 expansion 202.2; sustaining 21.8). [D006.10, p.36; D008.2, p.40; D008.3, p.44]
- Q107: Quantify PPA with NOA Group (3 July 2025, 10+5 years) cost commitment and start date; FY27 electricity step-up. [D006.10, p.36; D008.1, p.39]
- Q108 (remainder): Confirm STI 137,867 treatment in net debt; FY27 FV assumption. [D006.10, p.35–36; D008.1, p.38–39; D008.3, p.44]
- Q112 (remainder): Confirm rehab fund FV assumption and Adjusted EBITDA treatment; AISC shows reclamation accretion −0.6 (FY26). [D006.10, p.35–36; D008.2, p.40]
- Q114: Confirm AISC/electricity reflects external PPA only; quantify external electricity post solar disposal. [D006.11, p.36; D008.1, p.39]
- Q127 (remainder): Confirm FY27 by-product credit assumption (FY26 4.1). [D008.2, pp.40–41]
```

---

### 5. Baseline Forecast Inputs Captured Here

| Metric (US$m unless stated) | FY26 | FY25 |
| --- | --- | --- |
| Sustaining capital — group | 21.8 | 11.7 |
| Expansion capital — group | 202.2 | 156.2 |
| **Total capital — group** | **224.0** | **167.9** |
| Sustaining — Barberton Mines total | 12.6 | 8.6 |
| Expansion — Barberton Mines total | 27.5 | 19.1 |
| Total — Barberton Mines | 40.1 | 27.7 |
| Sustaining — Evander Mines total | 1.7 | 2.0 |
| Expansion — Evander Mines total | 69.2 | 45.9 |
| Total — Evander Mines | 70.9 | 47.9 |
| Sustaining — MTR | 2.7 | 0.3 |
| Expansion — MTR | 29.9 | 51.9 |
| Total — MTR | 32.6 | 52.2 |
| Sustaining — Tennant | 2.9 | – |
| Expansion — Tennant | 68.4 | 35.8 |
| Total — Tennant | 71.3 | 35.8 |
| Sustaining — Agricultural ESG | 0.1 | 0.3 |
| Expansion — Solar projects | 7.2 | 3.5 |
| Sustaining — Corporate | 1.8 | 0.5 |
| Cash and cash equivalents | (108.3) | (49.4) |
| Short-term investments | (137.9) | – |
| Borrowings | 51.5 | 190.0 |
| Financial instrument liability | – | 1.8 |
| Lease liability | 7.8 | 3.9 |
| Financial liability | 1.2 | 3.3 |
| Facility arrangement fees | – | 0.9 |
| **Net (cash)/debt** | **(185.7)** | **150.5** |
| **Net (cash)/senior debt** | **(194.7)** | **141.5** |
| Cash + STI (derived) | 246.2 | 49.4 |
| Gross debt (borrowings+lease+fin.liab.) | 60.5 | 199.0 |
| Net debt definition | Borrowings (pre-IFRS 9) less cash incl. FX/commodity derivatives | same |
| Net senior debt definition | Secured interest-bearing bank debt less available cash | same |

---

### 6. Next Section to Capture

**`D008.1` (Financial APMs, pp. 38–39)** — it is the single most useful next capture because it will resolve the highest-priority open items: **Q120/Q129/Q130/Q146/Q147/Q149/Q150/Q151/Q152/Q153** (net debt reconciliation, gold loan/trading/SBP/restricted cash treatment, IFRS 9 and hedge netting, borrowings-to-cash-flow tie), plus **Q119/Q121/Q122/Q123/Q128/Q131/Q132** (Adjusted EBITDA, FCF, LFCF, headline earnings reconciliations). If D008.1 is unavailable, capture **`D006.8` (Notes 15,16, pp. 31–33)** to resolve the borrowings/gold loan/gold trading composition directly.