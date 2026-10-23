# Section 11: Financial notes — Notes 15,16

> **Package**: `section-82186fa2d41b45e9ba07929593bcb7f0`  
> **Report**: `Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf` (annual_report)  
> **Model**: `deepseek/deepseek-v4.1-flash-1017`  
> **Execution Time**: 74.22s  
> **Cost**: $0.0041  
> **Tokens**: 19,128 total (9,238 prompt / 9,890 completion)  

### 1. Answers to Stored Questions for This Section

**Q82: Confirm no residual liability from Tennant debt settlement (24,917,607 shares to former lender); check Note 18 for any contingent consideration.**
- **Status**: `Partially resolved (remainder stays open for D006.9/D006.10 if Note 18 appears there)`
- **Answer & evidence**: Note 15 footnote [^1] confirms the 24,917,607 shares were issued "in settlement of an existing debt obligation" to a prior lender of Tennant in the *previous* reporting period (FY25), with US$10,877k credited to share premium [D006.8, p.31]. No residual liability is shown in Note 16 borrowings — the Northern Territory of Australia loan (US$7,049k) and National Australia Bank loan (US$2,342k) were both fully settled in FY26 (27 Feb 2026 and 30 June 2026 respectively) [D006.8, p.32]. **However**, Note 18 (Emmerson acquisition) is not in this capture, so contingent consideration cannot yet be confirmed. Carry forward.

**Q27 (remainder) / Q35: Resolve note 14/15 cross-reference and undefined [^2] footnote numbering gap.**
- **Status**: `Partially resolved`
- **Answer & evidence**: Note 15 in this section is "SHARE PREMIUM" and contains a single footnote [^1] (Tennant lender shares) plus unnumbered "Capital reduction" commentary blocks [D006.8, p.31]. Note 16.7 contains footnotes [^1], [^2], [^3] all defined in-section [D006.8, p.33]. The earlier [^2] gap referenced in Q27/Q35 (from D006.1/D006.7) is **not** resolved by this section — the numbering here is internally consistent. Remainder stays open for D006.1/D006.7 re-check.

**Q31 (remainder): Reconcile cash+STI US$246.2m and debt facilities US$78.9m to cash flow statement and Emmerson/equity issuance.**
- **Status**: `Partially resolved`
- **Answer & evidence**: Note 16 total borrowings carried at **US$51,535k** (FY26) vs US$189,977k (FY25) [D006.8, p.31]. This is the *carrying value*, not the *facility headroom* figure of US$78.9m cited earlier — the US$78.9m likely refers to drawn facilities or a different APM definition. Note 16.7 shows **total credit facilities of US$220,550k** (FY26) vs US$286,959k (FY25) [D006.8, p.33] — this is gross facility capacity, not debt. The reconciliation of US$78.9m to either US$51,535k carrying value or US$220,550k facilities is **not** established here. Carry forward to D008 (APM) for the net debt definition.

**Q47 (remainder): Check FY27 capex interest-capitalisation; FY27 finance cost run-rate (FY26 capitalisation nil vs FY25 7,190).**
- **Status**: `Partially resolved`
- **Answer & evidence**: FY26 finance costs by facility: RCF US$117k + term loan US$2,860k + DMTN US$6,364k + Realside US$2,952k + NT loan US$274k + NAB US$99k = **US$12,666k** gross finance costs incurred in FY26 [D006.8, pp.31–32]. Note the term loan, Realside, NT and NAB facilities were all settled during FY26, so FY27 run-rate should drop materially — only RCF (US$60k balance) and DMTN (US$51,475k) remain. **FY27 finance cost run-rate ≈ DMTN coupon + small RCF** — needs D008/D005.1 confirmation of the DMTN coupon rate. Carry forward.

**Q83 (remainder): Confirm treasury share treatment in EPS and dividend calculations; check if treasury shares will be cancelled or reissued.**
- **Status**: `Partially resolved`
- **Answer & evidence**: Note 15 confirms the share premium account was **cancelled in full** and appropriated to retained earnings, effective 21 May 2026 (FY26 capital reduction) and 18 July 2024 (FY25) [D006.8, p.31]. This creates distributable reserves but does **not** address treasury shares directly. Treasury share treatment in EPS/DPS remains open — carry forward.

**Q24 (remainder): Confirm reciprocal dividend (8,847) cash round-trip on 13.1% treasury; net vs gross; FY27 dividend policy.**
- **Status**: `Not addressed in this section` — carry forward.

**Q28 (remainder): Confirm split of cash vs STI 137,867 vs investments 12,791 vs restricted cash 2,612; reconcile to US$246.2m.**
- **Status**: `Not addressed in this section` — carry forward.

**Q44, Q52, Q67, Q69, Q77, Q78, Q79, Q80:**
- **Status**: `Not addressed in this section` — carry forward.

**Q59, Q13, Q23, Q41, Q76 (Emmerson Note 18):**
- **Status**: `Not addressed — Note 18 not in this capture` — carry forward.

---

### 2. Footnote & Qualification Deep-Dive

**Note 15, footnote [^1] — Tennant lender shares** [D006.8, p.31]:
> "During the previous reporting period, 24,917,607 shares were issued to a prior lender of Tennant company in settlement of an existing debt obligation."

- **What it changes**: Confirms the FY25 share premium movement of US$10,877k was a **non-cash debt-for-equity settlement**, not a cash raise. This means FY25 "Shares issued" of US$10,877k should be excluded from any free cash flow or equity raise analysis. It also confirms the Tennant debt settlement was completed in FY25, with no residual in FY26 borrowings.
- **Verification needed**: Confirm in Note 18 (Emmerson) whether any similar share-based consideration exists, and confirm the 24,917,607 shares are included in the FY26 weighted average share count (they were issued in FY25, so should be in both FY25 and FY26 weighted counts).

**Note 15, "Capital reduction" commentary** [D006.8, p.31]:
> "Formal approval of the capital reduction in the current reporting period was granted by the High Court... on 28 April 2025. The Court order... was registered with the Registrar of Companies on 21 May 2026, and therefore the capital reduction became effective on this date. Following the share capital reduction, the Company's share premium account was cancelled in full, with the amount appropriated to retained earnings."

- **What it changes**: The FY26 capital reduction of US$10,877k is a **non-cash reserve reclassification** (share premium → retained earnings), not a distribution. It creates distributable reserves, which is a **precondition for dividend payments**. This supports the FY26 dividend but does not itself represent a cash outflow. The FY25 capital reduction (US$235,063k) was similarly non-cash.
- **Forecast implication**: No P&L or cash flow impact. But it confirms the company now has distributable reserves to support the FY26 dividend and potentially FY27 dividends.
- **Verification needed**: Confirm in D005.1 (Statement of Changes in Equity) that the US$10,877k reclassification appears correctly and that retained earnings increased by that amount.

**Note 16.1 — RCF amendment and JIBAR→ZARONIA transition** [D006.8, p.31]:
> "The amendment extended the maturity date of the existing RCF of ZAR1 billion (US$54.1 million) to 30 June 2027."
> "Addenda to the relevant facility agreements were signed on 12 August 2026. The transition will take effect on the next interest rate reset rollover date of 29 September 2026. The change is not expected to result in a substantial modification under IFRS 9."

- **What it changes**: The RCF maturity is **30 June 2027** — i.e., it matures within FY27. This is a **near-term refinancing risk** that must be flagged. The ZAR1bn facility is only US$60k drawn at FY26 year-end, so the refinancing risk is about **availability**, not repayment. The JIBAR→ZARONIA transition is post-year-end (12 Aug 2026 addenda, effective 29 Sep 2026) and is not expected to be a substantial modification — so no P&L impact expected, but the **interest rate basis changes** from JIBAR to ZARONIA, which may alter the effective rate.
- **Verification needed**: Confirm in D008 (APM) or D003 (CEO statement) whether the RCF is expected to be renewed before 30 June 2027, and whether the ZARONIA transition changes the effective interest rate materially.

**Note 16.2 — Term loan settled** [D006.8, p.31]:
> "The term loan was settled during the current reporting period and the facility is no longer available."

- **What it changes**: The term loan (FY25: US$68,804k) was **fully repaid** in FY26 (repayment of capital US$73,025k). This is a **major debt reduction** — FY27 interest savings should be material. The facility is **no longer available**, so the group cannot redraw it. This reduces financial flexibility.
- **Forecast implication**: FY27 finance costs should drop by approximately the term loan's FY26 finance cost of US$2,860k (plus unwinding of fees US$813k). The US$73,025k repayment is a **cash outflow** in FY26 financing activities — confirm in D005.1 cash flow statement.

**Note 16.3 — DMTN bonds** [D006.8, p.32]:
> "PARS01 was fully settled and PARS03 was partially settled during the current reporting period."
> "The Group will proceed with amending and restating its applicable pricing supplements applicable to the DMTN bonds once legislation has been enacted for PARS02 and PARS03 regarding the transition from JIBAR to ZARONIA."

- **What it changes**: DMTN bonds reduced from US$67,972k to US$51,475k (settlement of US$20,990k). The **PARS02 and PARS03 JIBAR→ZARONIA transition is pending legislation** — this is a **future interest rate risk** that is not yet quantified. The current portion is US$12,896k (due within FY27), non-current US$38,579k.
- **Forecast implication**: FY27 DMTN finance cost run-rate ≈ US$6,364k (FY26 incurred) less the settled PARS01 portion. Need the coupon rates on PARS02/PARS03 to model accurately.
- **Verification needed**: Confirm in D008 or D005.1 the DMTN coupon rates and maturity profile for PARS02/PARS03.

**Note 16.4 — Realside facility settled 26 Feb 2026** [D006.8, p.32]:
- **What it changes**: US$31,856k capital repaid + US$2,890k finance costs repaid = **US$34,746k cash outflow** in FY26. This was an Australia-related facility (from the Tennant acquisition). Its settlement removes US$2,952k of FY26 finance costs from the FY27 run-rate.

**Note 16.5 — NT Australia loan settled 27 Feb 2026** [D006.8, p.32]:
- **What it changes**: US$7,094k capital + US$769k finance costs repaid = **US$7,863k cash outflow**. Removes US$274k FY26 finance costs from FY27 run-rate.

**Note 16.6 — NAB loan settled 30 June 2026** [D006.8, p.32]:
- **What it changes**: US$2,412k capital + US$133k finance costs repaid = **US$2,545k cash outflow**. Removes US$99k FY26 finance costs from FY27 run-rate.

**Note 16.7, footnote [^1] — Guarantees** [D006.8, p.33]:
> "The guarantees issued to Eskom Holdings SOC Limited relate to the supply of electricity. RMB issued a guarantee to Eskom on behalf of MTR resulting in an increase in the Eskom guarantee. The guarantees issued to the DMPR relate to the Group's environmental rehabilitation obligation."

- **What it changes**: The Eskom guarantee increased from US$3,761k to US$5,271k (+US$1,510k) — this is a **contingent liability** related to MTR electricity supply. The DMPR guarantee of US$40,575k (up from US$37,626k) is the **environmental rehabilitation obligation** — this is a real future cash cost, not just a guarantee. The increase of US$2,949k may reflect updated rehabilitation estimates.
- **Forecast implication**: The DMPR rehabilitation obligation is a **long-term liability** that should be modelled as a future cash outflow. The Eskom guarantee is a contingent liability — no cash impact unless called.
- **Verification needed**: Confirm in D006.5 (PPE) or D006.6 (provisions) the rehabilitation provision balance and whether the US$40,575k guarantee matches the provision.

**Note 16.7, footnote [^2] — General banking facility** [D006.8, p.33]:
> "The Nedbank Limited and RMB general banking facilities are unsecured and were unutilised in the current and previous reporting periods. These facilities, when utilised, bear interest at rates linked to the South African prime interest rate."

- **What it changes**: US$18,226k of undrawn, unsecured general banking facilities are **available liquidity** but not drawn. This is a **liquidity buffer** for FY27. The prime-linked rate means if drawn, cost would be prime + margin.

**Note 16.7, footnote [^3] — Gold and derivative trading facilities** [D006.8, p.33]:
> "The US$ gold and derivative trading facilities are used by the Group for the purpose of trading gold inventory and subsequent conversion of US$ sales proceeds into ZAR. The facilities are held at Absa Bank Limited, Nedbank Limited, Rand Merchant Bank Limited and Investec Bank Limited."

- **What it changes**: US$58,931k of gold trading facilities (up from US$35,003k) — this is a **significant increase** (+US$23,928k). These are used for **gold inventory trading and FX conversion**, not for debt funding. The increase may reflect higher gold prices (more value per ounce traded) or increased trading volumes. This is **not debt** and should not be included in net debt calculations.
- **Forecast implication**: The gold loan facility (US$25,557k, up from US$16,338k) is a **gold borrowing facility** — if drawn, it represents a gold price exposure. The increase of US$9,219k may indicate increased gold borrowing, which would be a **hedging/price exposure** item.
- **Verification needed**: Confirm in D008 (APM) whether the gold loan facility is included in net debt or treated as a trading facility. Confirm in D009 (production summary) whether gold borrowing affects reported sales volumes.

---

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| Q84 | High | D005.1 (Primary financial statements) | Term loan repayment US$73,025k + Realside US$31,856k + NT loan US$7,094k + NAB US$2,412k + RCF US$13,934k + DMTN US$20,990k = **US$149,311k total debt repayments** in FY26 [D006.8, pp.31–32] | Check cash flow statement financing activities for total debt repayments; confirm the US$149,311k sum and reconcile to net debt movement | Confirms FY26 cash outflow from debt reduction; critical for FY27 net debt forecast |
| Q85 | High | D005.1 (Primary financial statements) | FY26 gross finance costs incurred: RCF 117 + term 2,860 + DMTN 6,364 + Realside 2,952 + NT 274 + NAB 99 = **US$12,666k** [D006.8, pp.31–32] | Check P&L net finance costs line; confirm gross finance costs US$12,666k less interest income = net finance costs; confirm FY26 capitalisation nil | Anchors FY27 finance cost run-rate (only RCF + DMTN remain) |
| Q86 | High | D008 (APM) | RCF maturity **30 June 2027** — matures within FY27; ZAR1bn (US$54.1m) facility only US$60k drawn [D006.8, p.31] | Check D008/D003 for RCF renewal/refinancing plans; confirm FY27 liquidity headroom | Near-term refinancing risk; affects FY27 going-concern and liquidity forecast |
| Q87 | Medium | D008 (APM) | JIBAR→ZARONIA transition: RCF addenda signed 12 Aug 2026, effective 29 Sep 2026; DMTN PARS02/PARS03 pending legislation [D006.8, pp.31–32] | Check D008 for any quantified interest rate impact; confirm whether ZARONIA rate differs materially from JIBAR | Affects FY27 finance cost forecast; potential margin change |
| Q88 | Medium | D006.5 / D006.6 (PPE / Provisions) | DMPR guarantee US$40,575k (up from US$37,626k, +US$2,949k) relates to environmental rehabilitation obligation [D006.8, p.33, fn 1] | Check rehabilitation provision balance in D006.5/D006.6; confirm whether US$40,575k guarantee matches provision; confirm FY27 rehabilitation cash spend | Long-term cash liability; affects FY27+ cash flow forecast |
| Q89 | Medium | D008 (APM) | Gold loan facility US$25,557k (up from US$16,338k, +US$9,219k); US$ gold trading facilities US$58,931k (up from US$35,003k) [D006.8, p.33] | Check D008 net debt definition — are gold loan/trading facilities included in net debt or excluded as trading? Confirm gold borrowing volumes | Affects net debt calculation and gold price exposure; potential hedging impact |
| Q90 | Medium | D005.1 (Primary financial statements) | Share premium cancelled in full: FY26 US$10,877k, FY25 US$235,063k appropriated to retained earnings [D006.8, p.31] | Check Statement of Changes in Equity for the US$10,877k reclassification; confirm retained earnings increase and distributable reserves | Confirms dividend capacity; no cash impact but supports FY27 dividend forecast |
| Q91 | Low | D006.9/D006.10 (if Note 18 appears) | Note 18 (Emmerson) not in this capture — contingent consideration, PPA, goodwill/bargain purchase still unverified [D006.8, p.31–33] | Locate Note 18 in subsequent pages; extract total consideration, FV net assets, goodwill vs bargain gain, PPA provisional/final | Critical for FY27 Emmerson contribution and balance sheet |
| Q92 | Low | D005.1 (Primary financial statements) | 24,917,607 Tennant lender shares issued in FY25 [D006.8, p.31, fn 1] | Confirm these shares are in FY26 weighted average share count (issued FY25, so should be in both years); check EPS denominator | Affects EPS and DPS per share calculations |

---

### 4. Updated Open Questions Ledger (Copy to App)

```markdown
# OPEN QUESTIONS LEDGER — after D006.8 (Notes 15,16)

## Pending: D005.1 (Primary financial statements)
- Q52: Extract pre-tax profit from P&L; compute FY26/FY25 ETR; confirm 33.2%/28.5%. [D006.4, p.25]
- Q24 (remainder): Confirm reciprocal dividend (8,847) cash round-trip on 13.1% treasury; net vs gross; FY27 dividend policy. [D005.1, p.18–19; D006.7, p.30]
- Q25 (remainder): Extract FY26 SBP P&L charge and FY27 expected charge; explain "Other expenses" 85,958 vs 36,484. [D005.1, p.17–18; D006.2, p.21,23]
- Q28 (remainder): Confirm split of cash vs STI 137,867 vs investments 12,791 (resolved: 12,705 CuFe + 86 associate) vs restricted cash 2,612; reconcile to US$246.2m. [D005.1, p.17–18; D006.1, p.19; D006.6, p.29; D006.7, p.30]
- Q31 (remainder): Reconcile cash+STI US$246.2m and debt facilities US$78.9m to cash flow statement and Emmerson/equity issuance. Note 16 carrying value US$51,535k vs facilities US$220,550k — US$78.9m definition unresolved. [D006.1, p.19; D006.8, p.31,33]
- Q44: Reconcile segment net assets 1,017,559 + goodwill 18,438 = 1,035,997 to group total equity. [D006.2, p.22]
- Q67: Reconcile "Inventory recognised in cost of production" 57,468 vs 27,358 (+US$30,110k) to cost of sales in P&L and production volumes. [D006.6, p.29]
- Q69: Check cash flow statement for VAT/GST receivable 18,107 timing and expected FY27 unwind. [D006.6, p.29]
- Q77: Confirm FY27 weighted average share count including 102,641,421 Emmerson shares issued 1 July 2026; check EPS and DPS calculations. [D006.7, p.30]
- Q78: Confirm share buy-back cash cost (~US$1,322k) in cash flow statement financing activities; check if further buy-backs planned FY27. [D006.7, p.30]
- Q79: Confirm working capital movement for other payables +US$29,480k in cash flow statement; check if accruals unwind in FY27. [D006.7, p.30]
- Q80: Confirm VAT payable US$5,836k payment timing in cash flow statement; check jurisdiction (Australia vs South Africa). [D006.7, p.30]
- Q83 (remainder): Confirm treasury share treatment in EPS and dividend calculations; check if treasury shares will be cancelled or reissued. Note 15 confirms share premium cancelled but not treasury shares. [D006.7, p.30; D006.8, p.31]
- Q84: Check cash flow statement financing activities for total debt repayments US$149,311k (term 73,025 + Realside 31,856 + NT 7,094 + NAB 2,412 + RCF 13,934 + DMTN 20,990); reconcile to net debt movement. [D006.8, pp.31–32]
- Q85: Check P&L net finance costs line; confirm gross finance costs US$12,666k (RCF 117 + term 2,860 + DMTN 6,364 + Realside 2,952 + NT 274 + NAB 99) less interest income = net finance costs; confirm FY26 capitalisation nil. [D006.8, pp.31–32]
- Q90: Check Statement of Changes in Equity for US$10,877k share premium cancellation reclassification to retained earnings; confirm distributable reserves. [D006.8, p.31]
- Q92: Confirm 24,917,607 Tennant lender shares (issued FY25) are in FY26 weighted average share count; check EPS denominator. [D006.8, p.31, fn 1]

## Pending: D008 (Alternative performance measures)
- Q2: Obtain AISC reconciliation (by operation and group); confirm vs guidance US$1,820–1,870/oz. [D002, p.3]
- Q11: Confirm renewable energy US$5.1m in FY26 base; water savings US$1.4m/yr incremental FY27+. [D002, p.2–3]
- Q20: Reconcile Elikhulu US$1,231/oz, MTR US$1,389/oz, BTRP US$1,564/oz to group AISC. [D003, p.6]
- Q34 (remainder): Confirm page 72 APM reconciliation; AISC/APM definitions tie to IFRS. [D006.1, p.19; D006.2, p.22,24]
- Q36: Confirm Adjusted EBITDA definition; restate FY25 (249,724 + 2,954 = 252,678). [D006.2, p.22,24]
- Q40: Confirm no FY27 solar segment; electricity cost step-up post-disposal; disposal gain/loss; solar capex 7,159 in FY26. [D006.2, p.20–21; D006.6, p.29]
- Q42: Confirm segment AISC/APMs before or after intra-group management fee allocation. [D006.2, p.21]
- Q47 (remainder): Check FY27 capex interest-capitalisation; FY27 finance cost run-rate. FY26 gross finance costs US$12,666k; term/Realside/NT/NAB settled, only RCF+DMTN remain. Need DMTN coupon rates. [D006.4, p.25; D006.8, pp.31–32]
- Q50: Confirm restricted cash 2,612 nature; finance income 60 FY26 vs nil FY25. [D006.4, p.25]
- Q57: Confirm ZAR/AUD FX rate FY26 close vs FY25; FY27 FX sensitivity on DTL. [D006.4, p.26]
- Q63: Confirm AISC uses production D&A US$60,288k (not total PPE depreciation US$61,733k); identify US$2,179k "other D&A". [D006.5, p.28]
- Q64: Confirm no further FY27 impairment; check CGU headroom assumptions. [D006.5, p.28]
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
- Q72: Confirm solar projects status at FY26 year-end, disposal timing/gain, FY27 electricity cost step-up. [D006.6, p.29]
- Q75: Confirm nature/collectability of other receivables 7,828 (Evander/Barberton); loss allowance adequacy. [D006.6, p.29]
- Q81: Confirm whether STI FV gain US$1,142k is excluded from Adjusted EBITDA/AISC; confirm STI treatment in net debt calculation. [D006.7, p.30]
- Q86: Check D008/D003 for RCF renewal/refinancing plans before 30 June 2027 maturity; confirm FY27 liquidity headroom. [D006.8, p.31]
- Q87: Check D008 for quantified JIBAR→ZARONIA interest rate impact; confirm whether ZARONIA differs materially from JIBAR. [D006.8, pp.31–32]
- Q89: Check D008 net debt definition — are gold loan facility US$25,557k and gold trading facilities US$58,931k included in net debt or excluded as trading? Confirm gold borrowing volumes. [D006.8, p.33]

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
- Q46: Confirm July 2026 deliveries against contract liability 8,030 included in FY27 ounces/revenue, not double-counted. [D006.3, p.25]
- Q48: Reconcile Australia revenue 132,804 to Tennant segment revenue in D006.2. [D006.3, p.25, fn 1]
- Q65: Extract segment-level D&A from Note 3 to split Tennant/Emmerson vs SA. [D006.5, p.28]
- Q66: Confirm FY27 tailings/stockpile feed assumption; quantify tailings contribution to FY26 ounces. [D006.6, p.29]
- Q67: Reconcile inventory charged to production 57,468 to production volumes. [D006.6, p.29]
- Q70: Confirm FY27 Tennant capex guidance and completion status. [D006.6, p.29]
- Q71: Confirm FY27 MTR and Elikhulu capex guidance. [D006.6, p.29]

## Pending: D002 / D003 (Highlights / CEO statement)
- Q3: Reconcile dividend implied share counts: 2,436m / 2,333m / 2,420m; issued/weighted count, Emmerson shares, treasury. [D002, p.2; D006.7, p.30]
- Q4: Confirm FX rate/date for dividend US$ conversion (implied ~16.40–16.46 vs stated avg 16.90). [D002, p.2]
- Q8: Confirm Soweto Cluster DFS gold price assumption; FID timing Dec 2026; financing plan; capex post-FY27. [D002, p.3]
- Q12: Quantify SBP expense FY26 vs FY25 and FY27 assumption. [D002, p.3]
- Q16: Locate Tennant FY27 capex $ for fixed crusher, secondary mill, belt filter; capitalised vs expensed. [D003, p.6]
- Q19: Extract total FY27 group capex guidance and Tennant-specific split (FY26 actual 223,995 captured). [D003, p.6; D006.6, p.29]

## Pending: D002 / D005.1 (Emmerson)
- Q22: RESOLVED — "Shares to be issued" US$148,218k relates to Emmerson. [D005.1, p.17,19; D006.7, p.30]

## Pending: D006.9/D006.10 (if Note 18 appears)
- Q59: Locate Note 18 — Emmerson acquisition: total consideration, FV net assets, goodwill vs bargain purchase gain, PPA provisional or final. [D006.5, p.27; D006.7, p.30]
- Q13 (remainder): Confirm Emmerson consolidation date (22 Jun 2026), consideration split, goodwill/PPA/bargain, FY27 contribution. [D002, p.3; D005.1, p.17,19; D006.2, p.20; D006.5, p.27; D006.7, p.30]
- Q23 (remainder): Confirm Emmerson consideration split, FV net assets, goodwill vs bargain gain. [D005.1, p.17; D006.2, p.20; D006.5, p.27; D006.7, p.30]
- Q41: Confirm Emmerson consideration, FV net assets, goodwill vs bargain, FY27 exploration/royalty contribution. [D006.2, p.20; D006.5, p.27; D006.7, p.30]
- Q76: Locate Note 18.1: extract total consideration, FV net assets, goodwill vs bargain purchase gain, PPA provisional or final. [D006.7, p.30]
- Q82 (remainder): Confirm no residual liability from Tennant debt settlement; check Note 18 for any contingent consideration. [D006.7, p.30; D006.8, p.31]
- Q91: Locate Note 18 in subsequent pages; extract total consideration, FV net assets, goodwill vs bargain gain, PPA provisional/final. [D006.8, pp.31–33]

## Pending: D006.5 / D006.6 (PPE / Provisions)
- Q88: Check rehabilitation provision balance in D006.5/D006.6; confirm whether US$40,575k DMPR guarantee matches provision; confirm FY27 rehabilitation cash spend. [D006.8, p.33, fn 1]

## Pending: D006.1 / D006.7 (Note numbering)
- Q27 (remainder): Resolve note 14/15 cross-reference and undefined [^2] footnote numbering gap. Note 15/16 numbering internally consistent; earlier gap unresolved. [D006.1, p.19–20; D006.7, p.30; D006.8, p.31]
- Q35: Confirm whether footnote definitions for Notes 1–2 exist on adjacent pages; resolve [^2] gap. [D006.1, p.19–20; D006.7, p.30]
```

---

### 5. Baseline Forecast Inputs Captured Here

| Item | FY26 | FY25 | Source |
| --- | --- | --- | --- |
| Share premium balance (opening) | 10,877 | 235,063 | [D006.8, p.31] |
| Capital reduction (non-cash) | (10,877) | (235,063) | [D006.8, p.31] |
| Shares issued (Tennant lender, non-cash) | – | 10,877 | [D006.8, p.31] |
| Share premium balance (closing) | – | 10,877 | [D006.8, p.31] |
| **Total borrowings (carrying value)** | **51,535** | **189,977** | [D006.8, p.31] |
| — RCF | 60 | 13,988 | [D006.8, p.31] |
| — Term loan | – | 68,804 | [D006.8, p.31] |
| — DMTN bonds | 51,475 | 67,972 | [D006.8, p.31] |
| — Realside facility | – | 29,822 | [D006.8, p.31] |
| — NT Australia loan | – | 7,049 | [D006.8, p.31] |
| — NAB loan | – | 2,342 | [D006.8, p.31] |
| Current portion of borrowings | 12,957 | 86,335 | [D006.8, p.31] |
| Non-current portion | 38,578 | 103,642 | [D006.8, p.31] |
| RCF facility size (ZAR1bn) | US$54.1m | – | [D006.8, p.31] |
| RCF maturity | 30 Jun 2027 | – | [D006.8, p.31] |
| Term loan settled | FY26 | – | [D006.8, p.31] |
| Realside settled | 26 Feb 2026 | – | [D006.8, p.32] |
| NT loan settled | 27 Feb 2026 | – | [D006.8, p.32] |
| NAB loan settled | 30 Jun 2026 | – | [D006.8, p.32] |
| DMTN PARS01 fully settled; PARS03 partially settled | FY26 | – | [D006.8, p.32] |
| **Gross finance costs incurred FY26** | **12,666** | – | [D006.8, pp.31–32] |
| — RCF | 117 | 4,189 | [D006.8, p.31] |
| — Term loan | 2,860 | 7,649 | [D006.8, p.31] |
| — DMTN | 6,364 | 6,963 | [D006.8, p.32] |
| — Realside | 2,952 | 3,228 | [D006.8, p.32] |
| — NT loan | 274 | 283 | [D006.8, p.32] |
| — NAB | 99 | 32 | [D006.8, p.32] |
| **Total debt repayments FY26 (capital)** | **149,311** | – | [D006.8, pp.31–32] |
| — Term loan | 73,025 | 3,662 | [D006.8, p.31] |
| — Realside | 31,856 | – | [D006.8, p.32] |
| — RCF | 13,934 | 65,696 | [D006.8, p.31] |
| — DMTN | 20,990 | 24,936 | [D006.8, p.32] |
| — NT loan | 7,094 | – | [D006.8, p.32] |
| — NAB | 2,412 | – | [D006.8, p.32] |
| **Total credit facilities (gross capacity)** | **220,550** | **286,959** | [D006.8, p.33] |
| — RCF | 60,753 | 56,388 | [D006.8, p.33] |
| — Term facility | – | 69,577 | [D006.8, p.33] |
| — Eskom guarantee | 5,271 | 3,761 | [D006.8, p.33] |
| — DMPR guarantee (rehab) | 40,575 | 37,626 | [D006.8, p.33] |
| — General banking facility (unutilised) | 18,226 | 7,887 | [D006.8, p.33] |
| — Gold hedging facility | 5,772 | 15,211 | [D006.8, p.33] |
| — US$ gold/derivatives trading facilities | 58,931 | 35,003 | [D006.8, p.33] |
| — Gold loan facility | 25,557 | 16,338 | [D006.8, p.33] |
| — Australia facilities (Realside/NT/NAB) | – | 39,930 | [D006.8, p.33] |
| JIBAR→ZARONIA RCF effective date | 29 Sep 2026 | – | [D006.8, p.31] |
| JIBAR→ZARONIA DMTN status | Pending legislation | – | [D006.8, p.32] |

---

### 6. Next Section to Capture

**`D006.9` (or next available Note 18 / Emmerson acquisition note)** — this will resolve the highest-priority open items: **Q59, Q13, Q23, Q41, Q76, Q82 (remainder), Q91** (Emmerson consideration, FV net assets, goodwill vs bargain purchase, PPA provisional/final, contingent consideration). If Note 18 is not in D006.9, capture **`D008` (Alternative Performance Measures)** next to resolve **Q2, Q34, Q36, Q47, Q86, Q87, Q89** (AISC reconciliation, net debt definition, RCF refinancing, ZARONIA impact, gold facility treatment).