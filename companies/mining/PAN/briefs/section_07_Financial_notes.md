# Section 07: Financial notes — Note 6. INCOME TAX

> **Package**: `section-5e760c827e0a452f92ae37d65f7ff278`  
> **Report**: `Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf` (annual_report)  
> **Model**: `deepseek/deepseek-v4.1-flash-1017`  
> **Execution Time**: 39.69s  
> **Cost**: $0.0024  
> **Tokens**: 11,958 total (6,606 prompt / 5,352 completion)  

### 1. Answers to Stored Questions for This Section

**Q26 (remainder) / Q32 / Q39 — Deferred tax liability +110m drivers; FY27 expected effective tax rate**
- **Status**: `Partially resolved (remainder stays open for D008/D009)`
- **Answer & evidence**: The +US$109,974k movement in net DTL (140,506 → 250,480) is driven almost entirely by **PPE temporary differences: 136,460 → 255,589 (+US$119,129k)** [D006.4, p.26]. The reconciliation confirms: opening 140,506 + DTL recognised in P&L 97,377 + FX translation 13,083 − transferred from DTA 486 = 250,480 [D006.4, p.26]. So the DTL build is (a) P&L deferred tax charge of ~97.4m (vs 36.3m in FY25 — a 2.7x step-up) and (b) a US$13.1m FX translation reserve movement (ZAR/AUD strengthening on ZAR/AUD-denominated DTLs). The PPE driver is consistent with the Australia non-current asset step-up (+US$209m per prior ledger) and accelerated capitalisation. **FY27 expected ETR is NOT stated in this section** — the deferred tax note gives rates applied (Barberton 28.29%, Evander 29.03%, MTR 29.95%, Tennant 30.00%, Other 27.00%) but no forward ETR guidance. Remainder stays open for D008 (APM/tax reconciliation) and D009.

**Q49 — Note 13 STI balance / FVTPL classification / 1,142 FV gain recurring**
- **Status**: `Not resolved in this section`
- **Answer & evidence**: This section (Note 6 Income Tax) does not contain Note 13 or the STI balance. The only tangential evidence is a **"Fair value adjustment on investment" DTL of 569 (FY26) vs nil (FY25)** [D006.4, p.26], which implies a fair-value gain on an investment was recognised in FY26 and taxed — consistent with (but not confirming) the 1,142 FV gain referenced in the stored question. Carry forward to D008/D009.

**Q50 — Restricted cash 2,612 / finance income 60 FY26 vs nil FY25**
- **Status**: `Not resolved in this section`
- **Answer & evidence**: Note 6 does not address restricted cash or finance income. Carry forward.

**Q51 — Other receivables 41,654 composition**
- **Status**: `Not resolved in this section`
- **Answer & evidence**: Note 6 does not address other receivables. Carry forward.

**Q24, Q25, Q27, Q28, Q29, Q30, Q31, Q33, Q35, Q38, Q43, Q44** — none of these are addressed by Note 6 evidence; carry forward unchanged.

---

### 2. Footnote & Qualification Deep-Dive

**Footnote [^1] — p.26 (DTL table and DTA table)**
- **Quote**: *"In the previous reporting period, employee obligations, cash-settled share-based payment obligations and the expected credit loss allowance were incorrectly classified as an environmental rehabilitation obligation. These items have been disaggregated in the current reporting period, with comparative figures restated accordingly."* [D006.4, p.26]
- **What it changes**: The FY25 comparative DTL line items are **restated**, not as originally reported. This means any FY25 DTL build analysis using previously published figures will not tie. Critically, the restatement **removes an "environmental rehabilitation obligation" DTL line entirely** — the current table has no such line. This raises a verification question: where is the rehabilitation provision DTL now carried (is it inside "Other" at (81), or was it reclassified out)? The restated FY25 employee obligations DTL is (2,283), cash-settled SBP (1,768), ECL (48) — all small. The restatement is presentational, not a change in total net DTL (140,506 unchanged), but it obscures the rehabilitation DTL quantum.
- **Must verify in later sections**: Whether the rehabilitation provision deferred tax is disclosed elsewhere (provisions note) and whether it is material to the FY27 DTL run-rate.

**Footnote [^1] — p.26 (DTA table)**
- **Quote**: *"Other payables previously included the temporary difference arising from the accrual for employee benefits and leave pay liability. This amount has been disaggregated in the current reporting period, with comparative figures restated accordingly."* [D006.4, p.26]
- **What it changes**: Same restatement theme — FY25 DTA "Other payables" (545) is restated and a new "Employee obligations" DTA line (626) appears. Small magnitudes; no forecast impact beyond confirming comparatives are not clean.

**Unnumbered qualification — p.26 (DTA recognition)**
- **Quote**: *"Deferred tax assets have only been recognised, where applicable, on the basis that the individual Group companies will be able to generate future taxable economic benefits to utilise current deductible temporary differences."* [D006.4, p.26]
- **What it changes**: Confirms DTA recognition is entity-by-entity and contingent on future taxable profits. Net DTA is only 1,921 — immaterial. But it signals that **assessed losses dropped from 6,729 (FY25) to 3 (FY26)** — i.e., the group has largely consumed its tax losses, which is a key reason the **current tax charge jumped from 19,348 to 73,486 (+280%)** and the **effective tax rate rose**. This is a structural step-up, not a one-off: FY27 current tax should be modelled on the higher, loss-depleted base.

**Footnote [^2] marker on "Other payables" DTA line (91)** — the footnote text for [^2] is **NOT present in this section capture**. The [^1] footnote appears twice but there is no [^2] definition printed. This is a **missing footnote** — flag as a verification question (consistent with the pre-existing Q27/Q35 numbering-gap concern).

**Arithmetic checks performed:**
- DTL reconciliation: 140,506 + 97,377 + 13,083 − 486 = **250,480** ✓ ties.
- DTA reconciliation: 2,072 + 205 − 486 + 130 = **1,921** ✓ ties.
- P&L deferred tax per 6.1 = 97,172; per DTL reconciliation = 97,377; per DTA reconciliation = 205. Net = 97,377 − 205 = **97,172** ✓ ties to 6.1.
- Current tax: SA 73,486 + Aus 6,799 = **80,285**; + deferred 97,172 = **177,457** ✓ ties to total income tax expense.
- **Tension flagged**: FY26 ETR = 177,457 / pre-tax profit. Pre-tax profit not in this section, but prior ledger noted FY26 ETR 33.2% vs FY25 28.5%. The jump is explained by (i) loss depletion (assessed loss DTA 6,729→3) and (ii) higher deferred tax on PPE. Verify pre-tax profit in D005.1 to confirm ETR.

---

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| Q52 | High | D005.1 (Primary financial statements) | Income tax expense 177,457 (FY26) vs 56,028 (FY25); ETR implied ~33%+ [D006.4, p.25] | Extract pre-tax profit from P&L; compute FY26 and FY25 ETR; confirm 33.2%/28.5% per prior ledger | Anchors FY27 tax line in forecast; confirms structural ETR step-up |
| Q53 | High | D008 (APM) / D006.2 | Assessed loss DTA collapsed 6,729→3; current tax +280% [D006.4, p.26] | Confirm no remaining tax losses; check whether FY27 current tax should be modelled at full statutory rates with no loss shield | Determines whether FY27 tax is a step-up vs FY26 or flat |
| Q54 | Medium | D006.2 / D008 | DTL PPE +119,129 driven by Australia non-current asset step-up (+209m) [D006.4, p.26] | Confirm Tennant/Emmerson PPE additions driving DTL; check whether FY27 capex adds further DTL | Deferred tax charge is now ~55% of total tax; capex drives it |
| Q55 | Medium | D006.2 / provisions note | Footnote [^1] removes "environmental rehabilitation obligation" DTL line; where is rehab DTL now? [D006.4, p.26] | Locate rehabilitation provision and its deferred tax in provisions/environmental note | Confirms no hidden DTL reclassification affecting FY27 |
| Q56 | Low | D006.4 adjacent pages / D006.1 | [^2] footnote marker on DTA "Other payables" (91) has NO printed definition in this capture [D006.4, p.26] | Locate [^2] definition on adjacent page or confirm numbering gap (links to Q27/Q35) | Completeness of note; minor |
| Q57 | Medium | D008 / D009 | FX translation reserve movement +13,083 on DTL [D006.4, p.26] | Confirm ZAR/AUD FX rate used for FY26 close vs FY25; assess FY27 FX sensitivity on DTL | DTL is FX-sensitive; forecast FX deck (Q30) affects deferred tax |
| Q58 | Low | D006.2 | Deferred tax rates applied: Barberton 28.29% (up from 24.00%), Evander 29.03%, MTR 29.95% [D006.4, p.26] | Confirm why Barberton rate stepped up 24%→28.29%; check if FY27 rate stable | Rate change affects FY27 deferred tax on Barberton PPE |

---

### 4. Updated Open Questions Ledger (Copy to App)

```markdown
# OPEN QUESTIONS LEDGER — after D006.4 (Note 6 Income Tax)

## Pending: D005.1 (Primary financial statements)
- Q52: Extract pre-tax profit from P&L; compute FY26/FY25 ETR; confirm 33.2%/28.5%. [D006.4, p.25]
- Q24 (remainder): Confirm reciprocal dividend (8,847) cash round-trip on 13.1% treasury; net vs gross; FY27 dividend policy. [D005.1, p.18–19]
- Q25 (remainder): Extract FY26 SBP P&L charge and FY27 expected charge; explain "Other expenses" 85,958 vs 36,484. [D005.1, p.17–18; D006.2, p.21,23]
- Q28 (remainder): Confirm split of cash vs STI 137,867 vs investments 12,791 vs restricted cash 2,612; reconcile to US$246.2m. [D005.1, p.17–18; D006.1, p.19]
- Q29 (remainder): Confirm drivers of other receivables 41,654 (contract liability 8,030 resolved). [D005.1, p.17; D006.3, p.25]
- Q31 (remainder): Reconcile cash+STI US$246.2m and debt facilities US$78.9m to cash flow statement and Emmerson/equity issuance. [D006.1, p.19]
- Q51: Locate note detailing other receivables 41,654 composition. [D005.1, p.17]

## Pending: D006.1 / D006.2 (Financial notes)
- Q26 (remainder): FY27 expected effective tax rate — NOT stated in Note 6; check D008/D009. [D006.1, p.19–20]
- Q27 (remainder): Resolve note 14/15 cross-reference and undefined [^2] footnote numbering gap. [D006.1, p.19–20]
- Q32: FY27 ETR from deferred tax note — partially resolved (rates given, no forward ETR). [D006.1, p.19–20]
- Q33 (remainder): Check PPE/impairment note for FY26 impairment/reversal, CGU carrying values, discount rate/price assumptions. [D006.1, p.20; D006.2, p.21–24]
- Q35: Confirm whether footnote definitions for Notes 1–2 exist on adjacent pages; resolve [^2] gap. [D006.1, p.19–20]
- Q38: Extract Australian PPE depreciation run-rate and Emmerson asset FV; confirm FY27 D&A step-up. [D006.2, p.24]
- Q39: FY27 ETR, mining tax vs corporate tax split — partially resolved (rates given). [D006.2, p.21,23]
- Q43: Confirm no CGU impairment/reversal in FY26; extract CGU carrying values and discount rate/price assumptions. [D006.2, p.21–24]
- Q44: Reconcile segment net assets 1,017,559 + goodwill 18,438 = 1,035,997 to group total equity. [D006.2, p.22]
- Q53: Confirm no remaining tax losses; model FY27 current tax at full statutory rates. [D006.4, p.26]
- Q54: Confirm Tennant/Emmerson PPE additions driving DTL +119,129; FY27 capex DTL impact. [D006.4, p.26]
- Q55: Locate rehabilitation provision deferred tax (removed from DTL table via restatement). [D006.4, p.26]
- Q56: Locate [^2] footnote definition on DTA "Other payables" (91). [D006.4, p.26]
- Q58: Confirm why Barberton deferred tax rate stepped 24.00%→28.29%; FY27 stability. [D006.4, p.26]

## Pending: D008 (Alternative performance measures)
- Q2: Obtain AISC reconciliation (by operation and group); confirm vs guidance US$1,820–1,870/oz. [D002, p.3]
- Q11: Confirm renewable energy US$5.1m in FY26 base; water savings US$1.4m/yr incremental FY27+. [D002, p.2–3]
- Q20: Reconcile Elikhulu US$1,231/oz, MTR US$1,389/oz, BTRP US$1,564/oz to group AISC. [D003, p.6]
- Q34 (remainder): Confirm page 72 APM reconciliation; AISC/APM definitions tie to IFRS. [D006.1, p.19; D006.2, p.22,24]
- Q36: Confirm Adjusted EBITDA definition; restate FY25 (249,724 + 2,954 = 252,678). [D006.2, p.22,24]
- Q40: Confirm no FY27 solar segment; electricity cost step-up post-disposal; disposal gain/loss. [D006.2, p.20–21]
- Q42: Confirm segment AISC/APMs before or after intra-group management fee allocation. [D006.2, p.21]
- Q47: Check FY27 capex interest-capitalisation; FY27 finance cost run-rate (FY26 capitalisation nil vs FY25 7,190). [D006.4, p.25]
- Q49: Extract Note 13 STI balance; confirm FVTPL; whether 1,142 FV gain recurring. [D006.4, p.25]
- Q50: Confirm restricted cash 2,612 nature; finance income 60 FY26 vs nil FY25. [D006.4, p.25]
- Q57: Confirm ZAR/AUD FX rate FY26 close vs FY25; FY27 FX sensitivity on DTL. [D006.4, p.26]

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
- Q37: Confirm Tennant FY27 capex guidance; crusher/mill/filter complete or continuing. [D006.2, p.22]
- Q45: Confirm FY26 Tennant full-year production/grade to anchor FY27 run-rate. [D006.2, p.23]
- Q46: Confirm July 2026 deliveries against contract liability 8,030 included in FY27 ounces/revenue, not double-counted. [D006.3, p.25]
- Q48: Reconcile Australia revenue 132,804 to Tennant segment revenue in D006.2. [D006.3, p.25, fn 1]

## Pending: D002 / D003 (Highlights / CEO statement)
- Q3: Reconcile dividend implied share counts: 2,436m / 2,333m / 2,420m; issued/weighted count, Emmerson shares, treasury. [D002, p.2]
- Q4: Confirm FX rate/date for dividend US$ conversion (implied ~16.40–16.46 vs stated avg 16.90). [D002, p.2]
- Q8: Confirm Soweto Cluster DFS gold price assumption; FID timing Dec 2026; financing plan; capex post-FY27. [D002, p.3]
- Q12: Quantify SBP expense FY26 vs FY25 and FY27 assumption. [D002, p.3]
- Q16: Locate Tennant FY27 capex $ for fixed crusher, secondary mill, belt filter; capitalised vs expensed. [D003, p.6]
- Q19: Extract total FY27 group capex guidance and Tennant-specific split. [D003, p.6]

## Pending: D002 / D005.1 (Emmerson)
- Q13 (remainder): Confirm Emmerson consolidation date (22 Jun 2026), consideration split, goodwill/PPA/bargain, FY27 contribution. [D002, p.3; D005.1, p.17,19; D006.2, p.20]
- Q22: Confirm "Shares to be issued" US$148,218k relates to Emmerson; number of shares, issue price, timing. [D005.1, p.17,19]
- Q23 (remainder): Confirm Emmerson consideration split, FV net assets, goodwill vs bargain gain. [D005.1, p.17; D006.2, p.20]
- Q41: Confirm Emmerson consideration, FV net assets, goodwill vs bargain, FY27 exploration/royalty contribution. [D006.2, p.20]

## Pending: D006.1 (going-concern deck)
- Q30: Confirm FY27 budget gold price deck (base US$4,600→US$4,900/oz; downside US$3,680/oz +10% production cut) and FX assumption; decide forecast deck. [D006.1, p.19]
```

---

### 5. Baseline Forecast Inputs Captured Here

| Item | FY26 | FY25 | Source |
| --- | --- | --- | --- |
| SA current tax | 73,486 | 19,348 | [D006.4, p.25] |
| — current year | 73,551 | 19,354 | |
| — prior year | (65) | (6) | |
| Australian current tax | 6,799 | 371 | |
| — current year | 6,817 | 371 | |
| — prior year | (18) | – | |
| Deferred tax (P&L) | 97,172 | 36,309 | |
| — current year | 97,071 | 33,438 | |
| — prior year | 101 | 2,871 | |
| **Total income tax expense** | **177,457** | **56,028** | |
| Net DTL at 30 June | 250,480 | 140,506 | [D006.4, p.26] |
| Net DTA at 30 June | 1,921 | 2,072 | |
| DTL PPE temporary difference | 255,589 | 136,460 | |
| DTL inventory | 2,577 | 9,080 | |
| DTL FX translation movement | 13,083 | 3,008 | |
| DTA assessed loss | 3 | 6,729 | |
| Deferred tax rates: Barberton | 28.29% | 24.00% | |
| Deferred tax rates: Evander | 29.03% | 28.00% | |
| Deferred tax rates: MTR | 29.95% | 28.00% | |
| Deferred tax rates: Tennant | 30.00% | 30.00% | |
| Deferred tax rates: Other | 27.00% | 27.00% | |

---

### 6. Next Section to Capture

**`D005.1` (Primary financial statements, p.17–19)** — resolves **Q52** (pre-tax profit → ETR confirmation), **Q24/Q25/Q28/Q29/Q31** (dividend, SBP, cash/STI, receivables, cash-flow reconciliation), and provides the P&L base needed to model FY27 tax. If D005.1 is unavailable, **`D008` (APM, p.38–47)** resolves **Q2, Q34, Q36, Q49, Q50, Q53, Q57** and the FY27 ETR/APM reconciliation.