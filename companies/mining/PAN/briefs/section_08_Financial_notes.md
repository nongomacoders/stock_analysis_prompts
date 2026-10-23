# Section 08: Financial notes — Note 7. PROPERTY, PLANT AND EQUIPMENT

> **Package**: `section-f71a7b0072dd49bc97184fd2838c56a9`  
> **Report**: `Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf` (annual_report)  
> **Model**: `deepseek/deepseek-v4.1-flash-1017`  
> **Execution Time**: 44.76s  
> **Cost**: $0.0029  
> **Tokens**: 14,647 total (8,777 prompt / 5,870 completion)  

### 1. Answers to Stored Questions for This Section

**Q33 (remainder) — Check PPE/impairment note for FY26 impairment/reversal, CGU carrying values, discount rate/price assumptions.**
- **Status**: `Partially resolved (remainder stays open for D008/D009)`
- **Answer & evidence**: Note 7 confirms FY26 **impairment losses of US$345k** (all in "Capital under construction" column) and **no reversal of impairment** in FY26 (FY25 had a net reversal of US$2,954k). No CGU-level carrying values, discount rates, or price assumptions are disclosed in this PPE note — those must be sought in the impairment note (likely Note 8/9, not captured) or D008. [D006.5, p.28]

**Q38 — Extract Australian PPE depreciation run-rate and Emmerson asset FV; confirm FY27 D&A step-up.**
- **Status**: `Partially resolved (Emmerson FV partially; Australian depreciation split not isolated)`
- **Answer & evidence**: Total FY26 depreciation on PPE = **US$61,733k** vs FY25 **US$34,394k** — a **+79% step-up**, consistent with a full year of Tennant + ~1 week of Emmerson. Emmerson additions through acquisition = **US$142,436k** (of which mineral rights/exploration US$142,244k; ROU assets US$112k; other US$80k) — this is the FV of Emmerson PPE acquired, not the full consideration. The note does **not** split Australian vs South African depreciation; that split must come from D006.2 segment note or D008. FY27 D&A will step up further on a full year of Emmerson + Tennant capex. [D006.5, p.27–28]

**Q43 — Confirm no CGU impairment/reversal in FY26; extract CGU carrying values and discount rate/price assumptions.**
- **Status**: `Partially resolved (impairment confirmed; CGU detail not in this note)`
- **Answer & evidence**: FY26 impairment = **US$345k** (capital under construction only); **no reversal**. CGU carrying values, discount rates and price decks are **not disclosed in Note 7** — carry forward to the impairment note / D008. [D006.5, p.28]

**Q54 — Confirm Tennant/Emmerson PPE additions driving DTL +119,129; FY27 capex DTL impact.**
- **Status**: `Partially resolved (additions confirmed; DTL link not in this note)`
- **Answer & evidence**: FY26 total PPE **additions = US$223,995k** (vs FY25 US$169,202k), plus **US$142,436k via acquisitions** (Emmerson). Capital under construction additions = **US$111,542k**; plant & machinery owned additions = **US$44,824k**. These are the gross capex drivers behind the deferred tax movement; the DTL reconciliation itself sits in Note 6 (D006.4). [D006.5, p.27]

**Q13 / Q23 / Q41 (Emmerson) — consideration split, FV net assets, goodwill vs bargain.**
- **Status**: `Partially resolved (FV of PPE acquired confirmed; consideration/goodwill not in this note)`
- **Answer & evidence**: Emmerson PPE acquired at FV = **US$142,436k**, dominated by **mineral rights & mining property US$142,244k** — i.e., the value is almost entirely in the mining property/exploration asset, not plant. This is a key input to the PPA/goodwill calculation but the consideration and goodwill/bargain figures are in Note 18 (referenced by [^1]) — carry forward. [D006.5, p.27]

**Q44 — Reconcile segment net assets to group total equity.**
- **Status**: `Not resolvable here` — Note 7 gives PPE carrying amount only (US$1,196,474k), not net assets. Carry forward to D005.1/D006.2.

**Q30 — FY27 budget gold price deck / FX.**
- **Status**: `Not addressed in this section` — no price/FX assumptions in Note 7. Carry forward.

*(All other stored questions relate to sections not in this capture and are carried forward in Section 4.)*

---

### 2. Footnote & Qualification Deep-Dive

- **`[^1]` on "Additions through acquisitions" (US$142,436k)** — `[D006.5, p.27]`. The footnote text reads only "Refer to note 18." **Note 18 is not in this capture.** This is the single most consequential footnote in the section: it is the gateway to the Emmerson business-combination disclosure (consideration, FV of net assets, goodwill vs bargain purchase, and whether any of the US$142,244k mineral rights is a provisional PPA allocation subject to remeasurement within 12 months). **Implication**: the US$142,436k is a *provisional* FV that could be revised; if a bargain purchase gain exists it would flow through P&L and distort FY26 earnings and the FY27 base. **Verification required**: locate Note 18 in a later capture (D006.6+ or D007) to confirm consideration, goodwill/bargain, and whether the PPA is final or provisional.

- **"Derecognition" of US$4,301k cost / US$3,725k accumulated depreciation (net ~US$576k)** — `[D006.5, p.27–28]`. No footnote explains what was derecognised. The ROU buildings/infrastructure line shows a US$2,953k cost derecognition offset by US$3,094k accumulated depreciation reversal — a **net credit** to the ROU asset. This looks like a lease termination/modification. **Implication**: check whether this is a one-off lease exit (e.g., solar plant disposal referenced in Q40) that changes the FY27 ROU depreciation and lease liability run-rate. **Verification required**: confirm nature of derecognition in the leases note (not captured).

- **"Transfers" net US$2,584k cost / net −US$2,661k accumulated depreciation** — `[D006.5, p.27–28]`. Large gross transfers (e.g., US$61,388k into plant & machinery owned, US$59,795k out of capital under construction) confirm **capital under construction is being commissioned into depreciable plant**. **Implication**: this is the mechanism by which FY27 depreciation steps up — assets moving from non-depreciating CUWIP (US$234,145k carrying at 30 Jun 2026) into depreciable plant. **Verification required**: confirm in D008/D009 the commissioning schedule of the US$234m CUWIP (Tennant crusher/mill/filter, White Devil) to time the FY27 D&A step-up.

- **"Increase in environmental rehabilitation obligation" US$6,520k added to PPE cost** — `[D006.5, p.27]`. This is an asset-retirement-cost capitalisation (mineral rights US$5,042k + buildings US$1,305k + exploration US$173k). **Implication**: it inflates PPE and the rehabilitation provision simultaneously; the related deferred tax was flagged as removed from the DTL table in Q55. **Verification required**: confirm the rehabilitation provision balance and its deferred tax treatment in the provisions note (not captured).

- **Depreciation reconciliation to cost of production** — `[D006.5, p.28]`. Total D&A in cost of production = **US$60,288k** (FY26) vs **US$33,360k** (FY25). Note the **"Add back: other depreciation and amortisation" of US$2,179k** — this is a reconciling item that removes non-production D&A from the cost-of-production figure. **Implication**: for AISC/unit-cost modelling, use US$60,288k as the production D&A, not the US$61,733k total PPE depreciation. The US$2,179k add-back is the D&A sitting outside cost of production (e.g., corporate/exploration). **Verification required**: confirm in D008 that AISC uses the US$60,288k figure.

---

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| Q59 | High | D006.6+ / D007 (Note 18) | `[^1]` "Refer to note 18" — Emmerson acquisition FV US$142,436k, mineral rights US$142,244k `[D006.5, p.27]` | Locate Note 18: extract total consideration, FV of net assets acquired, goodwill vs bargain purchase gain, and whether PPA is provisional | Determines whether FY26 earnings include a one-off bargain gain and whether FY27 base is clean |
| Q60 | High | D008 / D009 | Capital under construction carrying US$234,145k at 30 Jun 2026 `[D006.5, p.28]` | Confirm commissioning schedule of CUWIP (Tennant crusher/mill/filter, White Devil) and timing of transfer to depreciable plant | Times the FY27 D&A step-up and capex-to-production conversion |
| Q61 | Medium | D006.6+ (leases note) | Derecognition net ~US$576k; ROU buildings derecognition US$2,953k cost / US$3,094k accum. dep. `[D006.5, p.27–28]` | Confirm nature (lease termination/solar disposal) and impact on FY27 ROU depreciation and lease liability | Adjusts FY27 D&A and finance cost run-rate |
| Q62 | Medium | D006.6+ (provisions note) | Environmental rehabilitation obligation increase US$6,520k capitalised to PPE `[D006.5, p.27]` | Extract rehabilitation provision balance and deferred tax treatment (links Q55) | Affects FY27 rehabilitation accretion/amortisation and DTL |
| Q63 | Medium | D008 | D&A in cost of production US$60,288k vs total PPE depreciation US$61,733k; add-back US$2,179k `[D006.5, p.28]` | Confirm AISC uses US$60,288k production D&A; identify what the US$2,179k "other D&A" relates to | Unit-cost and AISC modelling accuracy |
| Q64 | Low | D006.2 / D008 | FY26 impairment US$345k (CUWIP only); no reversal `[D006.5, p.28]` | Confirm no further impairment in FY27 guidance; check CGU headroom assumptions | FY27 earnings risk if further impairment |
| Q65 | Low | D006.2 | Australian vs SA depreciation split not disclosed in Note 7 `[D006.5, p.28]` | Extract segment-level D&A from Note 3 to split Tennant/Emmerson vs SA | Segment margin and AISC-by-operation modelling |

---

### 4. Updated Open Questions Ledger (Copy to App)

```markdown
# OPEN QUESTIONS LEDGER — after D006.5 (Note 7 PPE)

## Pending: D005.1 (Primary financial statements)
- Q52: Extract pre-tax profit from P&L; compute FY26/FY25 ETR; confirm 33.2%/28.5%. [D006.4, p.25]
- Q24 (remainder): Confirm reciprocal dividend (8,847) cash round-trip on 13.1% treasury; net vs gross; FY27 dividend policy. [D005.1, p.18–19]
- Q25 (remainder): Extract FY26 SBP P&L charge and FY27 expected charge; explain "Other expenses" 85,958 vs 36,484. [D005.1, p.17–18; D006.2, p.21,23]
- Q28 (remainder): Confirm split of cash vs STI 137,867 vs investments 12,791 vs restricted cash 2,612; reconcile to US$246.2m. [D005.1, p.17–18; D006.1, p.19]
- Q29 (remainder): Confirm drivers of other receivables 41,654 (contract liability 8,030 resolved). [D005.1, p.17; D006.3, p.25]
- Q31 (remainder): Reconcile cash+STI US$246.2m and debt facilities US$78.9m to cash flow statement and Emmerson/equity issuance. [D006.1, p.19]
- Q51: Locate note detailing other receivables 41,654 composition. [D005.1, p.17]
- Q44: Reconcile segment net assets 1,017,559 + goodwill 18,438 = 1,035,997 to group total equity. [D006.2, p.22]

## Pending: D006.6+ / D007 (Note 18 and other notes)
- Q59: Locate Note 18 — Emmerson acquisition: total consideration, FV net assets, goodwill vs bargain purchase gain, PPA provisional or final. [D006.5, p.27, fn 1]
- Q60: Confirm commissioning schedule of CUWIP US$234,145k (Tennant crusher/mill/filter, White Devil); timing of transfer to depreciable plant. [D006.5, p.28]
- Q61: Confirm nature of derecognition (net ~US$576k; ROU buildings US$2,953k cost / US$3,094k accum. dep.); impact on FY27 ROU depreciation and lease liability. [D006.5, p.27–28]
- Q62: Extract rehabilitation provision balance and deferred tax treatment (links Q55). [D006.5, p.27]
- Q55: Locate rehabilitation provision deferred tax (removed from DTL table via restatement). [D006.4, p.26]
- Q56: Locate [^2] footnote definition on DTA "Other payables" (91). [D006.4, p.26]
- Q27 (remainder): Resolve note 14/15 cross-reference and undefined [^2] footnote numbering gap. [D006.1, p.19–20]
- Q35: Confirm whether footnote definitions for Notes 1–2 exist on adjacent pages; resolve [^2] gap. [D006.1, p.19–20]

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
- Q63: Confirm AISC uses production D&A US$60,288k (not total PPE depreciation US$61,733k); identify US$2,179k "other D&A". [D006.5, p.28]
- Q64: Confirm no further FY27 impairment; check CGU headroom assumptions. [D006.5, p.28]
- Q26 (remainder): FY27 expected effective tax rate — check D008/D009. [D006.1, p.19–20]
- Q32 (remainder): FY27 ETR from deferred tax note — rates given, no forward ETR. [D006.1, p.19–20]
- Q39 (remainder): FY27 ETR, mining tax vs corporate tax split. [D006.2, p.21,23]
- Q53: Confirm no remaining tax losses; model FY27 current tax at full statutory rates. [D006.4, p.26]
- Q58: Confirm why Barberton deferred tax rate stepped 24.00%→28.29%; FY27 stability. [D006.4, p.26]
- Q30: Confirm FY27 budget gold price deck (base US$4,600→US$4,900/oz; downside US$3,680/oz +10% production cut) and FX assumption; decide forecast deck. [D006.1, p.19]

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
- Q65: Extract segment-level D&A from Note 3 to split Tennant/Emmerson vs SA. [D006.5, p.28]

## Pending: D002 / D003 (Highlights / CEO statement)
- Q3: Reconcile dividend implied share counts: 2,436m / 2,333m / 2,420m; issued/weighted count, Emmerson shares, treasury. [D002, p.2]
- Q4: Confirm FX rate/date for dividend US$ conversion (implied ~16.40–16.46 vs stated avg 16.90). [D002, p.2]
- Q8: Confirm Soweto Cluster DFS gold price assumption; FID timing Dec 2026; financing plan; capex post-FY27. [D002, p.3]
- Q12: Quantify SBP expense FY26 vs FY25 and FY27 assumption. [D002, p.3]
- Q16: Locate Tennant FY27 capex $ for fixed crusher, secondary mill, belt filter; capitalised vs expensed. [D003, p.6]
- Q19: Extract total FY27 group capex guidance and Tennant-specific split. [D003, p.6]

## Pending: D002 / D005.1 (Emmerson)
- Q13 (remainder): Confirm Emmerson consolidation date (22 Jun 2026), consideration split, goodwill/PPA/bargain, FY27 contribution. [D002, p.3; D005.1, p.17,19; D006.2, p.20; D006.5, p.27]
- Q22: Confirm "Shares to be issued" US$148,218k relates to Emmerson; number of shares, issue price, timing. [D005.1, p.17,19]
- Q23 (remainder): Confirm Emmerson consideration split, FV net assets, goodwill vs bargain gain. [D005.1, p.17; D006.2, p.20; D006.5, p.27]
- Q41: Confirm Emmerson consideration, FV net assets, goodwill vs bargain, FY27 exploration/royalty contribution. [D006.2, p.20; D006.5, p.27]
```

---

### 5. Baseline Forecast Inputs Captured Here

| Metric | FY26 | FY25 | Source |
| --- | --- | --- | --- |
| PPE cost — closing balance | 1,536,566 | 1,082,411 | [D006.5, p.27] |
| PPE accumulated dep. & impairment — closing | (340,092) | (257,961) | [D006.5, p.28] |
| **PPE carrying amount — closing** | **1,196,474** | **824,450** | [D006.5, p.28] |
| Additions (organic) | 223,995 | 169,202 | [D006.5, p.27] |
| Additions through acquisitions (Emmerson) | 142,436 | 99,404 | [D006.5, p.27] |
| — of which mineral rights & mining property | 142,244 | 31,628 | [D006.5, p.27] |
| Capital under construction additions | 111,542 | 148,019 | [D006.5, p.27] |
| Capital under construction carrying | 234,145 | 170,063 | [D006.5, p.28] |
| Depreciation on PPE | (61,733) | (34,394) | [D006.5, p.28] |
| Depreciation recognised in inventory | (487) | 646 | [D006.5, p.28] |
| Amortisation of intangibles | (247) | (126) | [D006.5, p.28] |
| Add back: other D&A | 2,179 | 514 | [D006.5, p.28] |
| **Total D&A in cost of production** | **(60,288)** | **(33,360)** | [D006.5, p.28] |
| Impairment losses (CUWIP) | (345) | — | [D006.5, p.28] |
| Reversal of impairment / (impairment) | — | (2,954) | [D006.5, p.28] |
| Environmental rehabilitation capitalised to PPE | 6,520 | 1,666 | [D006.5, p.27] |
| Borrowing costs capitalised | — | 7,190 | [D006.5, p.27] |
| Derecognition (net) | ~(576) | — | [D006.5, p.27–28] |
| FX translation reserve movement on PPE cost | 85,222 | 23,382 | [D006.5, p.27] |

---

### 6. Next Section to Capture

**`D006.6` (next financial note after Note 7, likely Note 8/9 impairment or Note 18 business combinations) or `D007`** — whichever contains **Note 18** (referenced by `[^1]`). This will resolve **Q59** (Emmerson consideration/goodwill/bargain), **Q13/Q23/Q41** (Emmerson PPA), and likely **Q33/Q43** (CGU impairment assumptions). If Note 18 is not in the next capture, prioritise **`D008`** to resolve **Q2/Q63** (AISC D&A treatment) and **Q30** (price deck).