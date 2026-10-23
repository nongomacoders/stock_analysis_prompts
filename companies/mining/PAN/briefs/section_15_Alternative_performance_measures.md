# Section 15: Alternative performance measures — FINANCIAL APMs

> **Package**: `section-b40a9b163106463997e21665e978461b`  
> **Report**: `Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf` (annual_report)  
> **Model**: `deepseek/deepseek-v4.1-flash-1017`  
> **Execution Time**: 97.61s  
> **Cost**: $0.0048  
> **Tokens**: 22,371 total (10,352 prompt / 12,019 completion)  

### 1. Answers to Stored Questions for This Section

- **Q2 & Q20 (AISC reconciliation by operation and group; confirm vs guidance US$1,820–1,870/oz; reconcile Elikhulu/MTR/BTRP to group AISC)**
  - **Status**: `Partially resolved (remainder stays open for D009)`
  - **Answer & evidence**: D008.1 provides the group AISC reconciliation at the "lower-cost vs higher-cost operations" level only, not by individual mine. FY26 group AISC = US$508,405k ÷ 272,373oz = **US$1,867/oz** [D008.1, p. 39]. This sits at the **top of the US$1,820–1,870/oz guidance range** (Q2 confirmed on the group number). Split: lower-cost operations US$420,686k ÷ 247,219oz = US$1,702/oz; higher-cost operations US$87,718k ÷ 25,154oz = US$3,487/oz. FY25 comparative: US$315,068k ÷ 196,927oz = US$1,600/oz (lower-cost US$1,434/oz; higher-cost US$2,598/oz). **The by-mine reconciliation (Elikhulu US$1,231/oz, MTR US$1,389/oz, BTRP US$1,564/oz) is NOT in this section** — it must be checked in D009 (Group production summary). Note the higher-cost bucket AISC deteriorated sharply YoY (US$2,598→US$3,487/oz) on lower ounces (28,146→25,154oz) — this is the "~US$3,500/oz tail" referenced in Q1 and needs mine-level attribution in D009.

- **Q34 (remainder) (Confirm APM reconciliation; AISC/APM definitions tie to IFRS)**
  - **Status**: `Partially resolved (remainder stays open for D008.2+)`
  - **Answer & evidence**: D008.1 confirms AISC is defined per the **World Gold Council** and is reconciled to "Cost of production" per IFRS, with adjustments for "other related costs as defined by the World Gold Council, including royalty costs, community costs, sustaining and development capital (excluding non-gold operations)" [D008.1, p. 38]. This confirms royalties ARE inside AISC (relevant to Q110). The actual line-by-line AISC reconciliation table (the "page 72 APM reconciliation" referenced in Q34) is **not in this capture** — still open.

- **Q36 (Confirm Adjusted EBITDA definition; restate FY25)**
  - **Status**: `Resolved (definition confirmed)`
  - **Answer & evidence**: Adjusted EBITDA = Profit after tax + income tax + depreciation & amortisation + net finance costs + impairment loss/reversals + bargain purchase gain + unrealised FV gains/losses on financial derivatives in the normal course of business [D008.1, p. 38]. Note: **SBP expense is NOT listed as an add-back** — so the US$57,272k SBP charge (Q101) sits INSIDE Adjusted EBITDA unless separately adjusted. The FY25 restatement arithmetic (249,724 + 2,954 = 252,678) cannot be re-verified here as the EBITDA reconciliation table is not in this capture.

- **Q63 (Confirm AISC uses production D&A US$60,288k, not total PPE depreciation US$61,733k; identify US$2,179k "other D&A")**
  - **Status**: `Partially resolved (definitional only)`
  - **Answer & evidence**: D008.1 confirms AISC reconciles to "Cost of production" (not total D&A), consistent with using production D&A. The specific US$60,288k vs US$61,733k split and the US$2,179k "other D&A" identification are **not in this capture** — still open for D008.2+ / D006.5.

- **Q81 (Confirm whether STI FV gain US$1,142k is excluded from Adjusted EBITDA/AISC; STI treatment in net debt)**
  - **Status**: `Partially resolved`
  - **Answer & evidence**: Adjusted EBITDA explicitly adds back "unrealised fair value gains or losses on financial derivatives undertaken in the normal course of business" [D008.1, p. 38] — so the STI FV gain is excluded from Adjusted EBITDA **if** the STI is classified as a derivative in the normal course. AISC is defined off "Cost of production" and does not reference FV gains, so the STI gain is **not** in AISC. Net debt definition (p. 39) references "cash and related hedges" and "financial liabilities" — STI treatment in net debt still needs confirmation in the net debt reconciliation table (not in this capture).

- **Q89 (Net debt definition — are gold loan facility US$25,557k and gold trading facilities US$58,931k included or excluded as trading?)**
  - **Status**: `Partially resolved (definition captured; application not yet verified)`
  - **Answer & evidence**: Net (cash)/debt = "Borrowings from financial institutions + IFRS 16 lease liabilities − cash and related hedges", adjusted for IFRS 9 accounting adjustments, restricted cash, and financial liabilities [D008.1, p. 39]. The definition is **facility-type agnostic** — it does not carve out gold loans or gold trading facilities as "trading". This suggests they may be included, but the actual net debt reconciliation table (with the US$25,557k and US$58,931k lines) is **not in this capture** — still open.

- **Q50 (Confirm restricted cash 2,612 nature)**
  - **Status**: `Partially resolved`
  - **Answer & evidence**: Net debt definition explicitly adjusts for "Restricted cash" [D008.1, p. 39] — confirming restricted cash is excluded from the cash netted against debt. The nature of the US$2,612k (Note 20.1) is not detailed here — still open.

- **Q86 (RCF renewal/refinancing plans before 30 June 2027 maturity; FY27 liquidity headroom)**
  - **Status**: `Not resolved here`
  - **Answer & evidence**: D008.1 defines "Net senior debt" (borrowings from financial institutions + IFRS 16 lease liabilities − net cash/senior debt, adjusted for IFRS 9, restricted cash, financial liabilities) [D008.1, p. 39] but contains **no commentary on RCF renewal or refinancing plans**. Still open for D008.2+ / D003.

- **Q87 (Quantified JIBAR→ZARONIA interest rate impact)**
  - **Status**: `Not resolved here`
  - **Answer & evidence**: No interest rate benchmark commentary in D008.1. Still open.

- **Q94 (Exploration asset carrying value US$142,244k; D008 AISC exclusion)**
  - **Status**: `Partially resolved (definitional)`
  - **Answer & evidence**: AISC is defined off "Cost of production" with World Gold Council adjustments; exploration asset carrying value/depletion is **not** an AISC line item per the definition [D008.1, p. 38]. Confirms exploration asset is excluded from AISC. The carrying value itself is not in this capture.

- **Q95 (Emmerson transaction costs US$11,879k capitalised; APM add-back/exclusion)**
  - **Status**: `Partially resolved (definitional)`
  - **Answer & evidence**: Adjusted EBITDA add-backs are limited to impairment, bargain purchase gain, and unrealised FV gains/losses [D008.1, p. 38]. **Transaction costs are NOT an explicit add-back** — so if capitalised (not in P&L), they are outside Adjusted EBITDA by construction; if any portion hit P&L, it would NOT be added back. Confirms no APM add-back for Emmerson costs. Still need to confirm capitalisation in D006.9 (already noted).

- **Q96 (Reconcile Note 18.2 "no disposals" against solar disposal expectation)**
  - **Status**: `Not resolved here`
  - **Answer & evidence**: No disposal commentary in D008.1. Still open.

- **Q100 (Cash-settled SBP current portion US$43,969k in net debt/liquidity)**
  - **Status**: `Partially resolved (definitional)`
  - **Answer & evidence**: Net debt definition adjusts for "financial liabilities" [D008.1, p. 39] — a cash-settled SBP liability could fall under this, but the definition is not explicit. Still needs confirmation in the net debt reconciliation table (not in this capture).

- **Q101 (SBP expense US$57,272k excluded from Adjusted EBITDA/AISC?)**
  - **Status**: `Resolved (definitional — NOT excluded)`
  - **Answer & evidence**: Adjusted EBITDA add-backs list does **not** include SBP expense [D008.1, p. 38]. Therefore the US$57,272k SBP charge **remains inside Adjusted EBITDA** and inside AISC (via cost of production). This is a material forecast point — FY27 SBP must be modelled as a real cost, not an add-back.

- **Q108 (STI 137,867 treatment in net debt and Adjusted EBITDA/AISC)**
  - **Status**: `Partially resolved (definitional)`
  - **Answer & evidence**: As per Q81 — unrealised FV gains/losses on derivatives are added back to Adjusted EBITDA [D008.1, p. 38]; STI is not in AISC (defined off cost of production). Net debt treatment still open (see Q89).

- **Q110 (Royalty cash outflow; whether royalties are in AISC)**
  - **Status**: `Resolved (definitional — royalties ARE in AISC)`
  - **Answer & evidence**: AISC adjustments explicitly include "**royalty costs**" [D008.1, p. 38]. This confirms royalties are inside AISC (consistent with Note 19 add-back of 14,609 and headline 712,119 being before royalties). FY27 royalty forecast should be modelled as an AISC component.

- **Q112 (Rehab fund FV assumption; gain excluded from Adjusted EBITDA?)**
  - **Status**: `Partially resolved (definitional)`
  - **Answer & evidence**: Adjusted EBITDA adds back "unrealised fair value gains or losses on financial derivatives undertaken in the normal course of business" [D008.1, p. 38]. A rehabilitation fund FV gain would only be excluded if classified as a derivative in the normal course — the definition does not explicitly cover rehab fund FV movements. Still needs confirmation.

- **Q114 (Whether AISC/electricity cost reflects external PPA only; external electricity cost post solar disposal)**
  - **Status**: `Not resolved here`
  - **Answer & evidence**: No electricity/PPA commentary in D008.1. Still open.

- **Q26/Q32/Q39/Q53/Q58 (FY27 ETR, tax split, tax losses, Barberton DTL rate)**
  - **Status**: `Not resolved here`
  - **Answer & evidence**: D008.1 contains no tax rate or ETR commentary. Still open for D008.2+ / D009.

- **Q30 (FY27 budget gold price deck)**
  - **Status**: `Not resolved here`
  - **Answer & evidence**: No price deck commentary in D008.1. Still open.

- **Q57 (ZAR/AUD FX rate FY26 close vs FY25)**
  - **Status**: `Not resolved here`
  - **Answer & evidence**: No FX rate commentary in D008.1. Still open.

- **Q40/Q72 (Solar segment, disposal timing/gain, electricity step-up)**
  - **Status**: `Not resolved here`
  - **Answer & evidence**: No solar commentary in D008.1. Still open.

- **Q42 (Segment AISC/APMs before or after intra-group management fee allocation)**
  - **Status**: `Not resolved here`
  - **Answer & evidence**: D008.1 gives only group-level lower-cost/higher-cost AISC, not segment-level. Still open for D009.

- **Q47 (remainder) (FY27 capex interest-capitalisation; finance cost run-rate)**
  - **Status**: `Not resolved here`
  - **Answer & evidence**: No finance cost commentary in D008.1. Still open.

- **Q64 (No further FY27 impairment; CGU headroom)**
  - **Status**: `Partially resolved (definitional)`
  - **Answer & evidence**: Adjusted EBITDA adds back "impairment loss or impairment reversals" [D008.1, p. 38] — confirming impairments are excluded from Adjusted EBITDA. No forward impairment commentary. Still open.

- **Q66/Q68/Q70/Q71/Q75 (Tailings feed, cyanide/prepayments, Tennant capex, MTR/Elikhulu capex, other receivables)**
  - **Status**: `Not resolved here`
  - **Answer & evidence**: No operational commentary in D008.1. Still open for D009.

- **Q102 (PAR Gold G-share vesting/settlement; I-share FY27 expense)**
  - **Status**: `Not resolved here`
  - **Answer & evidence**: No G-share/I-share commentary in D008.1. Still open.

- **Q105 (Board-approved commitments 309,076 and open orders 94,580 — which projects)**
  - **Status**: `Not resolved here`
  - **Answer & evidence**: No commitments commentary in D008.1. Still open.

- **Q107 (PPA with NOA Group cost commitment and start date)**
  - **Status**: `Not resolved here`
  - **Answer & evidence**: No PPA commentary in D008.1. Still open.

- **Q113 (Intra-group management fee and Evander Solar electricity charge eliminate on consolidation)**
  - **Status**: `Not resolved here`
  - **Answer & evidence**: No related-party commentary in D008.1. Still open.

- **Q11 (Renewable energy US$5.1m FY26 base; water savings US$1.4m/yr)**
  - **Status**: `Not resolved here`
  - **Answer & evidence**: No renewable energy/water savings commentary in D008.1. Still open for D002/D003.

---

### 2. Footnote & Qualification Deep-Dive

No footnote markers (`[^1]`, `*`) appear in the supplied D008.1 evidence. However, several embedded qualifications in the APM definitions carry material forecast implications:

- **AISC definition — "excluding non-gold operations"** [D008.1, p. 38]: The AISC adjustment explicitly excludes sustaining/development capital for non-gold operations. Since gold is 99.7% of revenue [D008.1, p. 38], this is immaterial for FY26 but must be checked in D009/D006.2 for any non-gold (e.g., chrome, PGM by-product) capital that is excluded from AISC but still consumes cash — a potential hidden cash drag not captured in AISC.

- **AISC definition — "value of by-product revenue is deducted from operating costs"** [D008.1, p. 39]: Confirms AISC is a **net** cost after by-product credits. For forecasting, any change in by-product (e.g., uranium, silver, chrome) prices/volumes will move AISC inversely. Need to check D009/D006.2 for by-product revenue quantum to model this sensitivity.

- **Adjusted EBITDA — SBP NOT an add-back** [D008.1, p. 38]: As flagged in Q101, the US$57,272k SBP charge sits inside Adjusted EBITDA. This is a **material** qualification: FY27 Adjusted EBITDA will be depressed by the FY27 SBP charge (which depends on share price and vesting). Forecast must model SBP as a real cost, not strip it out.

- **Adjusted EBITDA — "unrealised fair value gains or losses on financial derivatives undertaken in the normal course of business"** [D008.1, p. 38]: The qualifier "in the normal course of business" is important — it means hedging derivatives are added back, but speculative/non-normal-course derivatives are not. Need to confirm in D008.2+ whether the STI (137,867) and gold trading facilities (58,931) are classified as "normal course" derivatives for this purpose.

- **Free cash flow — "Less capital expenditure funded through permitted indebtedness"** [D008.1, p. 39]: This is a non-obvious adjustment. FCF is reduced by capex funded through permitted indebtedness — meaning debt-funded capex is treated as a cash outflow in FCF even though it may not hit the cash flow statement as capex. For FY27 forecasting, need to identify which capex (Tennant crusher/mill/filter, MTR expansion, solar) is "permitted indebtedness"-funded and therefore deducted in FCF but not in reported capex. This could create a gap between reported capex and FCF-deducted capex.

- **Free cash flow — "Adjusted for non-cash flow items as determined in accordance with IAS 7"** [D008.1, p. 39]: This is a catch-all that could include SBP, rehabilitation provisions, etc. Need to check the FCF reconciliation table (not in this capture) to see exactly which non-cash items are adjusted — particularly whether SBP is added back in FCF (even though it's not in Adjusted EBITDA).

- **Levered free cash flow — includes "Proceeds from borrowings" and "Repayment of borrowings"** [D008.1, p. 39]: This means LFCF is a **post-financing** metric. For FY27, the RCF maturity (30 June 2027) and any refinancing will flow through LFCF. Need to check D008.2+ for the LFCF reconciliation and whether the RCF repayment is modelled.

- **Net debt — "cash and related hedges"** [D008.1, p. 39]: The phrase "related hedges" is ambiguous — does it mean hedges related to cash (e.g., FX forwards on cash balances) or hedges related to debt (e.g., interest rate swaps)? This affects whether the STI (137,867) is netted against debt. Need to check the net debt reconciliation table.

- **Net debt — "Financial liabilities" adjustment** [D008.1, p. 39]: This is a broad catch-all. Could include the cash-settled SBP current portion (43,969), the gold loan facility (25,557), and gold trading facilities (58,931). Need to check the reconciliation table to confirm which financial liabilities are added to net debt.

- **Headline earnings — per SAICA Circular 1/2023** [D008.1, p. 39]: Confirms headline earnings is calculated per SAICA Circular 1/2023, with adjustments for (profit)/loss on disposal of PPE, impairment/reversals, bargain purchase gain, and tax effect. This is the JSE-listed headline EPS metric — relevant for dividend cover and valuation, but not directly for AISC/EBITDA forecasting.

- **"Portfolio complexity" — gold 99.7% of revenue** [D008.1, p. 38]: Confirms the group is essentially a pure gold play. For forecasting, this means the gold price deck (Q30) is the dominant revenue driver, and by-product credits are immaterial (<0.3% of revenue).

- **"Earnings volatility" — management excludes non-recurring items and quantifies uncontrollable factors** [D008.1, p. 38]: This is a forward-looking statement of intent — management will continue to present APMs that strip out price/FX volatility. For forecasting, this means reported APMs may diverge from IFRS numbers in FY27 if there are further "non-recurring" items (e.g., Emmerson integration costs, solar disposal gain).

---

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| Q118 | High | D008.2 (APM reconciliations, p. 40+) | AISC reconciliation table not in this capture — only lower-cost/higher-cost split given [D008.1, p. 39] | Locate the full AISC reconciliation table (cost of production → AISC) and confirm the line items: royalties, community costs, sustaining capex, development capex, by-product credits. Confirm the US$508,405k total ties to the sum of line items. | Needed to build a bottom-up FY27 AISC forecast and to verify Q2/Q20 by-mine reconciliation. |
| Q119 | High | D008.2 (APM reconciliations, p. 40+) | Adjusted EBITDA reconciliation table not in this capture — only definition given [D008.1, p. 38] | Locate the Adjusted EBITDA reconciliation and confirm: (a) SBP expense is NOT added back (per definition); (b) STI FV gain IS added back; (c) impairment add-back quantum; (d) FY25 restated EBITDA = 252,678. | Confirms Q36 and Q101; critical for FY27 EBITDA forecast. |
| Q120 | High | D008.2 (APM reconciliations, p. 40+) | Net debt reconciliation table not in this capture — only definition given [D008.1, p. 39] | Locate the net debt reconciliation and confirm treatment of: gold loan facility (25,557), gold trading facilities (58,931), STI (137,867), cash-settled SBP current portion (43,969), restricted cash (2,612), IFRS 16 lease liabilities. | Resolves Q89, Q100, Q108; critical for FY27 net debt and leverage forecast. |
| Q121 | High | D008.2 (APM reconciliations, p. 40+) | Free cash flow reconciliation not in this capture — definition includes "capex funded through permitted indebtedness" and "non-cash flow items per IAS 7" [D008.1, p. 39] | Locate the FCF reconciliation and identify: (a) which capex is "permitted indebtedness"-funded (Tennant, MTR, solar?); (b) which non-cash items are adjusted (SBP? rehab?); (c) reconcile FCF to cash flow statement. | Needed for FY27 FCF forecast and dividend cover; the "permitted indebtedness" adjustment could create a gap vs reported capex. |
| Q122 | Medium | D008.2 (APM reconciliations, p. 40+) | Levered free cash flow definition includes borrowings proceeds/repayments [D008.1, p. 39] | Locate the LFCF reconciliation and confirm whether the RCF repayment (30 June 2027 maturity) is modelled; confirm LFCF ties to net debt movement. | Resolves Q86 (RCF refinancing) and Q84 (debt repayments). |
| Q123 | Medium | D008.2 (APM reconciliations, p. 40+) | Headline earnings reconciliation not in this capture — definition per SAICA Circular 1/2023 [D008.1, p. 39] | Locate the headline earnings reconciliation and confirm: (a) profit/loss on disposal of PPE (solar disposal?); (b) impairment quantum; (c) tax effect; (d) headline EPS denominator (links Q77/Q93/Q117). | Needed for dividend cover and JSE valuation; confirms whether solar disposal gain flows through headline earnings. |
| Q124 | Medium | D009 (Group production summary) | AISC by-mine reconciliation (Elikhulu US$1,231/oz, MTR US$1,389/oz, BTRP US$1,564/oz) not in D008.1 [D008.1, p. 39] | In D009, locate the by-mine AISC table and reconcile each mine's AISC × ounces to the group US$508,405k. Confirm which mines sit in "lower-cost" (US$1,702/oz) vs "higher-cost" (US$3,487/oz) buckets. | Resolves Q2/Q20 remainder; needed for FY27 by-mine AISC forecast. |
| Q125 | Medium | D009 (Group production summary) | Higher-cost operations AISC deteriorated US$2,598→US$3,487/oz on lower ounces (28,146→25,154oz) [D008.1, p. 39] | In D009, identify which mines are in the higher-cost bucket and why AISC rose ~34% YoY. Confirm FY27 outlook for these mines (closure? turnaround?). | The "~US$3,500/oz tail" (Q1) is a drag on group AISC; FY27 forecast needs to know if it persists. |
| Q126 | Medium | D008.2 (APM reconciliations, p. 40+) | AISC definition "excluding non-gold operations" [D008.1, p. 38] | Confirm whether any non-gold capital (chrome, PGM, uranium by-product) is excluded from AISC but still consumes cash. Quantify if material. | Potential hidden cash drag not in AISC; affects FCF forecast. |
| Q127 | Medium | D008.2 (APM reconciliations, p. 40+) | AISC deducts by-product revenue [D008.1, p. 39] | Quantify by-product revenue (silver, chrome, uranium?) deducted from AISC. Confirm FY27 by-product assumption. | By-product credits reduce AISC; a change in by-product prices moves AISC inversely. |
| Q128 | Low | D008.2 (APM reconciliations, p. 40+) | "Unrealised FV gains/losses on financial derivatives undertaken in the normal course of business" add-back [D008.1, p. 38] | Confirm whether STI (137,867) and gold trading facilities (58,931) are classified as "normal course" derivatives for the add-back. Confirm FY26 add-back quantum. | Resolves Q81/Q108; affects Adjusted EBITDA forecast. |
| Q129 | Low | D008.2 (APM reconciliations, p. 40+) | "Financial liabilities" adjustment in net debt [D008.1, p. 39] | Confirm which financial liabilities are added to net debt (SBP? gold loan? trading facilities?). | Resolves Q89/Q100; affects net debt forecast. |
| Q130 | Low | D008.2 (APM reconciliations, p. 40+) | "Cash and related hedges" in net debt [D008.1, p. 39] | Confirm whether "related hedges" means FX hedges on cash or interest rate swaps on debt; confirm whether STI is netted. | Affects net debt definition and FY27 leverage. |
| Q131 | Low | D008.2 (APM reconciliations, p. 40+) | Rehab fund FV gain treatment in Adjusted EBITDA [D008.1, p. 38] | Confirm whether rehab fund FV movements are added back (as "normal course" derivatives) or left in EBITDA. | Resolves Q112; affects Adjusted EBITDA forecast. |
| Q132 | Low | D008.2 (APM reconciliations, p. 40+) | "Non-cash flow items as determined in accordance with IAS 7" in FCF [D008.1, p. 39] | Identify which non-cash items are adjusted in FCF (SBP? rehab? D&A already added back?). Confirm whether SBP is added back in FCF even though not in Adjusted EBITDA. | Affects FCF forecast; potential inconsistency between EBITDA and FCF treatment of SBP. |

---

### 4. Updated Open Questions Ledger (Copy to App)

```markdown
# OPEN QUESTIONS LEDGER — after D008.1 (Financial APMs, pp. 38–39)

## Pending: D008.2+ (APM reconciliations, pp. 40–47)
- Q118: Locate full AISC reconciliation table (cost of production → AISC); confirm line items (royalties, community, sustaining/development capex, by-product credits); tie US$508,405k total. [D008.1, p. 39]
- Q119: Locate Adjusted EBITDA reconciliation; confirm SBP NOT added back, STI FV gain added back, impairment quantum, FY25 restated 252,678. [D008.1, p. 38]
- Q120: Locate net debt reconciliation; confirm treatment of gold loan 25,557, gold trading 58,931, STI 137,867, cash-settled SBP 43,969, restricted cash 2,612, IFRS 16 leases. [D008.1, p. 39]
- Q121: Locate FCF reconciliation; identify "permitted indebtedness"-funded capex and IAS 7 non-cash adjustments; reconcile to cash flow statement. [D008.1, p. 39]
- Q122: Locate LFCF reconciliation; confirm RCF repayment (30 June 2027 maturity) modelled; tie to net debt movement. [D008.1, p. 39]
- Q123: Locate headline earnings reconciliation; confirm disposal/impairment/tax adjustments and EPS denominator. [D008.1, p. 39]
- Q126: Confirm non-gold capital excluded from AISC; quantify if material. [D008.1, p. 38]
- Q127: Quantify by-product revenue deducted from AISC; confirm FY27 assumption. [D008.1, p. 39]
- Q128: Confirm STI (137,867) and gold trading (58,931) classified as "normal course" derivatives for Adjusted EBITDA add-back. [D008.1, p. 38]
- Q129: Confirm which financial liabilities added to net debt (SBP? gold loan? trading?). [D008.1, p. 39]
- Q130: Confirm "cash and related hedges" meaning; whether STI netted in net debt. [D008.1, p. 39]
- Q131: Confirm rehab fund FV gain treatment in Adjusted EBITDA. [D008.1, p. 38]
- Q132: Identify IAS 7 non-cash items adjusted in FCF; confirm SBP treatment in FCF. [D008.1, p. 39]
- Q34 (remainder): Confirm page 72 APM reconciliation; AISC/APM definitions tie to IFRS. [D006.1, p.19; D006.2, p.22,24; D008.1, p.38–39]
- Q36 (remainder): Confirm FY25 restated Adjusted EBITDA 252,678 in reconciliation table. [D006.2, p.22,24; D008.1, p.38]
- Q63 (remainder): Confirm AISC uses production D&A US$60,288k (not total PPE depreciation US$61,733k); identify US$2,179k "other D&A". [D006.5, p.28; D006.10, p.35; D008.1, p.38]
- Q81 (remainder): Confirm STI FV gain US$1,142k excluded from Adjusted EBITDA/AISC; confirm STI treatment in net debt. [D006.7, p.30; D006.10, p.35; D008.1, p.38–39]
- Q86: Confirm RCF renewal/refinancing plans before 30 June 2027 maturity; FY27 liquidity headroom. [D006.8, p.31; D008.1, p.39]
- Q87: Quantify JIBAR→ZARONIA interest rate impact; confirm ZARONIA vs JIBAR. [D006.8, pp.31–32; D008.1, p.39]
- Q89 (remainder): Confirm gold loan 25,557 and gold trading 58,931 included/excluded from net debt. [D006.8, p.33; D008.1, p.39]
- Q94 (remainder): Confirm exploration asset carrying value US$142,244k; FY27 depletion/impairment; AISC exclusion confirmed. [D006.9, p.34; D008.1, p.38]
- Q95 (remainder): Confirm Emmerson transaction costs US$11,879k capitalised (not in P&L/Adjusted EBITDA); no APM add-back. [D006.9, p.34; D008.1, p.38]
- Q96: Reconcile Note 18.2 "no disposals" against solar disposal expectation; confirm timing/gain and FY27 electricity step-up. [D006.9, p.34; D008.1, p.39]
- Q100 (remainder): Confirm cash-settled SBP current portion US$43,969k in net debt/liquidity; FY27 cash settlement. [D006.9, p.33; D006.10, p.35; D008.1, p.39]
- Q101 (resolved definitional — SBP NOT excluded from Adjusted EBITDA/AISC; model as real cost). [D008.1, p.38]
- Q102: Confirm PAR Gold G-share vesting/settlement (11,541,455, vest 30 June 2026) in FY27 cash flow; I-share FY27 expense. [D006.9, p.34; D008.1, p.38]
- Q105: Identify projects for 309,076 board-approved commitments and 94,580 open orders; tie to FY27 capex. [D006.10, p.36; D008.1, p.39]
- Q107: Quantify PPA with NOA Group (3 July 2025, 10+5 years) cost commitment and start date; FY27 electricity step-up. [D006.10, p.36; D008.1, p.39]
- Q108 (remainder): Confirm STI 137,867 treatment in net debt; FY27 FV assumption. [D006.10, p.35–36; D008.1, p.38–39]
- Q110 (resolved definitional — royalties ARE in AISC; model as AISC component). [D008.1, p.38]
- Q112 (remainder): Confirm rehab fund FV assumption and Adjusted EBITDA treatment. [D006.10, p.35–36; D008.1, p.38]
- Q114: Confirm AISC/electricity reflects external PPA only; quantify external electricity post solar disposal. [D006.11, p.36; D008.1, p.39]
- Q26 (remainder): FY27 expected effective tax rate — check D008/D009. [D006.1, p.19–20]
- Q32 (remainder): FY27 ETR from deferred tax note. [D006.1, p.19–20]
- Q39 (remainder): FY27 ETR, mining tax vs corporate tax split. [D006.2, p.21,23]
- Q53: Confirm no remaining tax losses; model FY27 current tax at full statutory rates. [D006.4, p.26]
- Q58: Confirm Barberton deferred tax rate step 24.00%→28.29%; FY27 stability. [D006.4, p.26]
- Q30: Confirm FY27 budget gold price deck (base US$4,600→US$4,900/oz; downside US$3,680/oz +10% production cut) and FX assumption. [D006.1, p.19]
- Q57: Confirm ZAR/AUD FX rate FY26 close vs FY25; FY27 FX sensitivity on DTL. [D006.4, p.26]
- Q40: Confirm no FY27 solar segment; electricity cost step-up post-disposal; disposal gain/loss; solar capex 7,159 in FY26. [D006.2, p.20–21; D006.6, p.29; D006.10, p.36; D006.11, p.36]
- Q42: Confirm segment AISC/APMs before or after intra-group management fee allocation. [D006.2, p.21]
- Q47 (remainder): Check FY27 capex interest-capitalisation; FY27 finance cost run-rate; DMTN coupon rates. [D006.4, p.25; D006.8, pp.31–32]
- Q50 (remainder): Confirm restricted cash 2,612 nature; finance income 60 FY26 vs nil FY25. [D006.10, p.35; D008.1, p.39]
- Q64 (remainder): Confirm no further FY27 impairment; CGU headroom (Barberton land claim — Note 23). [D006.5, p.28; D006.11, p.36; D008.1, p.38]
- Q66: Confirm FY27 tailings/stockpile feed assumption; quantify tailings contribution to FY26 ounces. [D006.6, p.29]
- Q68: Check cyanide cost per tonne and prepayments 15,914 unwind in FY27; working capital movement. [D006.6, p.29]
- Q70: Confirm FY27 Tennant capex guidance; crusher/mill/filter/White Devil completion. [D006.6, p.29]
- Q71: Confirm FY27 MTR and Elikhulu capex guidance; MTR expansion completion. [D006.6, p.29]
- Q72: Confirm solar projects status at FY26 year-end, disposal timing/gain, FY27 electricity step-up. [D006.6, p.29; D006.10, p.36; D006.11, p.36]
- Q75: Confirm nature/collectability of other receivables 7,828 (Evander/Barberton); loss allowance adequacy. [D006.6, p.29]
- Q113: Confirm intra-group management fee and Evander Solar electricity charge eliminate on consolidation. [D006.11, p.36]

## Pending: D009 (Group production summary)
- Q1: Confirm total group ounces, Sheba+Consort ounces and AISC; reconcile to ~US$3,500/oz tail. [D002, p.2–3]
- Q2 (remainder): By-mine AISC reconciliation (Elikhulu US$1,231/oz, MTR US$1,389/oz, BTRP US$1,564/oz) to group US$508,405k. [D002, p.3; D008.1, p.39]
- Q6: Confirm Elikhulu 56,475oz @ US$1,231/oz and MTR 51,927oz @ US$1,389/oz full-year; MTR expansion run-rate FY27. [D002, p.3]
- Q9: Reconcile White Devil ~3Mt @ 3.8g/t (~350Koz) to 50→100Koz/yr ramp over 5 years. [D002, p.3]
- Q5 (remainder): Confirm Tennant FY27 capex $; White Devil first blast date and grade ramp. [D002, p.3; D003, p.6]
- Q7 (remainder): Confirm Evander underground grade >11g/t FY26 sustainability into FY27. [D002, p.3]
- Q10 (remainder): Confirm Royal Sheba first production timing; not double-counted with BTRP. [D002, p.3; D003, p.6]
- Q14: Check FY27 MTR production split; H1 FY27 below nameplate, Q2–Q4 step-up to ~60Koz annualised. [D003, p.6]
- Q15: Check FY27 BTRP guidance; flotation benefit FY27 or FY28. [D003, p.6]
- Q17: Check Elikhulu FY27 guidance vs FY26 56,475oz; Winkelhaak feed contribution. [D003, p.6]
- Q18: Check FY27 Tennant grade assumption and White Devil strip ratio/grade. [D003, p.6]
- Q20 (remainder): Reconcile Elikhulu/MTR/BTRP AISC to group AISC. [D003, p.6; D008.1, p.39]
- Q21: Confirm Fairview 47,678oz vs table 47,677oz rounding. [D003, p.6–7]
- Q37: Confirm Tennant FY27 capex guidance; crusher/mill/filter complete or continuing. [D006.2, p.22; D006.6, p.29]
- Q45: Confirm FY26 Tennant full-year production/grade to anchor FY27 run-rate. [D006.2, p.23]
- Q46: Confirm July 2026 deliveries against contract liability 8,030 included in FY27 ounces/revenue, not double-counted. [D006.3, p.25; D006.10, p.35]
- Q48: Reconcile Australia revenue 132,804 to Tennant segment revenue in D006.2. [D006.3, p.25, fn 1]
- Q65: Extract segment-level D&A from Note 3 to split Tennant/Emmerson vs SA. [D006.5, p.28]
- Q66: Confirm FY27 tailings/stockpile feed assumption; quantify tailings contribution to FY26 ounces. [D006.6, p.29]
- Q67: Reconcile inventory charged to production 57,468 to production volumes. [D006.6, p.29]
- Q70: Confirm FY27 Tennant capex guidance and completion status. [D006.6, p.29]
- Q71: Confirm FY27 MTR and Elikhulu capex guidance. [D006.6, p.29]
- Q97: Check D009 for any Emmerson/Tennant Creek ounces, exploration spend or royalty contribution in FY27 guidance; confirm not double-counted with Tennant. [D006.9, p.34]
- Q124: By-mine AISC table; reconcile each mine to group US$508,405k; confirm lower-cost vs higher-cost bucket membership. [D008.1, p.39]
- Q125: Identify higher-cost bucket mines; explain AISC rise US$2,598→US$3,487/oz; FY27 outlook. [D008.1, p.39]

## Pending: D005.1 (Primary financial statements)
- Q52: Extract pre-tax profit from P&L; compute FY26/FY25 ETR; confirm 33.2%/28.5%. [D006.4, p.25]
- Q24 (remainder): Confirm reciprocal dividend (8,847) cash round-trip on 13.1% treasury; net vs gross; FY27 dividend policy. [D005.1, p.18–19; D006.7, p.30; D006.11, p.36]
- Q25 (remainder): Extract FY26 SBP P&L charge and FY27 expected charge; explain "Other expenses" 85,958 vs 36,484. [D005.1, p.17–18; D006.2, p.21,23]
- Q31 (remainder): Reconcile cash+STI US$246.2m and debt facilities US$78.9m to cash flow statement and Emmerson/equity issuance. [D006.1, p.19; D006.8, p.31,33; D006.10, p.35]
- Q44: Reconcile segment net assets 1,017,559 + goodwill 18,438 = 1,035,997 to group total equity. [D006.2, p.22]
- Q67: Reconcile "Inventory recognised in cost of production" 57,468 vs 27,358 (+US$30,110k) to cost of sales in P&L and production volumes. [D006.6, p.29; D006.10, p.35]
- Q69: Check cash flow statement for VAT/GST receivable 18,107 timing and expected FY27 unwind. [D006.6, p.29; D006.10, p.35]
- Q77: Confirm FY27 weighted average share count including 102,641,421 Emmerson shares issued 1 July 2026; check EPS and DPS calculations. [D006.7, p.30; D006.9, p.34; D006.11, p.36]
- Q78: Confirm share buy-back cash cost (~US$1,322k) in cash flow statement financing activities; further buy-backs FY27. [D006.7, p.30]
- Q79: Confirm working capital movement for other payables +US$29,480k in cash flow statement; reconcile to Note 19 trade and other payables increase 50,354. [D006.7, p.30; D006.10, p.35]
- Q80: Confirm VAT payable US$5,836k payment timing in cash flow statement; jurisdiction. [D006.7, p.30]
- Q83 (remainder): Confirm treasury share treatment in EPS and dividend calculations; cancellation/reissue. [D006.7, p.30; D006.8, p.31]
- Q84: Check cash flow statement financing activities for total debt repayments US$149,311k; reconcile to net debt movement. [D006.8, pp.31–32; D006.10, p.35]
- Q85: Check P&L net finance costs line; reconcile Note 19 finance costs 17,318 and income (4,706) = net 12,612 vs D006.8 gross 12,666 (4,652 gap). [D006.8, pp.31–32; D006.10, p.35]
- Q90: Check SOCIE for US$10,877k share premium cancellation reclassification to retained earnings; distributable reserves. [D006.8, p.31]
- Q92: Confirm 24,917,607 Tennant lender shares (issued FY25) in FY26 weighted average share count; EPS denominator. [D006.8, p.31, fn 1]
- Q93: Confirm 102,641,421 Emmerson shares excluded from 30 June 2026 issued count and included in FY27 weighted average from 1 July 2026; EPS/DPS denominators. [D006.9, p.34; D006.11, p.36]
- Q98: Confirm reserve for shares to be issued US$148,218k presented in equity (Note 14) and reconciles to SOCIE; no cash outflow. [D006.9, p.34]
- Q103: Identify missing ~43,831 FY26 adjustment line in Note 19 "Adjusted for" subtotal 143,482. [D006.10, p.35]
- Q109: Confirm FY27 payables unwind assumption; reconcile Note 19 trade and other payables increase 50,354 to D006.7 29,480. [D006.10, p.35; D006.7, p.30]
- Q117: Confirm FY27 weighted average share count and EPS/DPS denominators include 102,641,421 Emmerson shares from 1 July 2026. [D006.11, p.36]

## Pending: D002 / D003 (Highlights / CEO statement)
- Q3: Reconcile dividend implied share counts: 2,436m / 2,333m / 2,420m; issued/weighted count, Emmerson shares, treasury. [D002, p.2; D006.7, p.30; D006.9, p.34]
- Q4: Confirm FX rate/date for dividend US$ conversion (implied ~16.40–16.46 vs stated avg 16.90). [D002, p.2]
- Q8: Confirm Soweto Cluster DFS gold price assumption; FID timing Dec 2026; financing plan; capex post-FY27. [D002, p.3]
- Q11: Confirm renewable energy US$5.1m in FY26 base; water savings US$1.4m/yr incremental FY27+. [D002, p.2–3]
- Q12: Quantify SBP expense FY26 vs FY25 and FY27 assumption. [D002, p.3; D006.9, p.33]
- Q16: Locate Tennant FY27 capex $ for fixed crusher, secondary mill, belt filter; capitalised vs expensed. [D003, p.6]
- Q19: Extract total FY27 group capex guidance and Tennant-specific split (FY26 actual 223,995 captured). [D003, p.6; D006.6, p.29]
- Q115: Confirm 8,847 reciprocal dividend is intra-group (eliminated), not external cash outflow; treasury-share mechanics. [D006.11, p.36]
- Q116: Confirm no provision/impairment for Barberton CGU or Evander litigation; contingent liability quantum. [D006.11, p.36]
```

---

### 5. Baseline Forecast Inputs Captured Here

| Metric | FY26 | FY25 | Source |
| --- | --- | --- | --- |
| Group AISC (US$k) | 508,405 | 315,068 | [D008.1, p. 39] |
| Group gold sold (oz) | 272,373 | 196,927 | [D008.1, p. 39] |
| Group AISC (US$/oz) | 1,867 | 1,600 | [D008.1, p. 39] |
| Lower-cost operations AISC (US$k) | 420,686 | 241,957 | [D008.1, p. 39] |
| Lower-cost gold sold (oz) | 247,219 | 168,781 | [D008.1, p. 39] |
| Lower-cost AISC (US$/oz) | 1,702 | 1,434 | [D008.1, p. 39] |
| Higher-cost operations AISC (US$k) | 87,718 | 73,111 | [D008.1, p. 39] |
| Higher-cost gold sold (oz) | 25,154 | 28,146 | [D008.1, p. 39] |
| Higher-cost AISC (US$/oz) | 3,487 | 2,598 | [D008.1, p. 39] |
| Gold % of group revenue | 99.7% | — | [D008.1, p. 38] |
| AISC guidance range (FY26) | US$1,820–1,870/oz | — | [D002, p. 3] (referenced) |
| AISC definition basis | World Gold Council; reconciles to IFRS "Cost of production" | — | [D008.1, p. 38] |
| AISC adjustments include | Royalty costs, community costs, sustaining & development capital (excl. non-gold ops); by-product revenue deducted | — | [D008.1, p. 38–39] |
| Adjusted EBITDA add-backs | Income tax, D&A, net finance costs, impairment/reversals, bargain purchase gain, unrealised FV gains/losses on normal-course derivatives | — | [D008.1, p. 38] |
| SBP expense in Adjusted EBITDA? | **No add-back — remains inside** | — | [D008.1, p. 38] |
| Net debt definition | Borrowings from financial institutions + IFRS 16 leases − cash & related hedges; adj. IFRS 9, restricted cash, financial liabilities | — | [D008.1, p. 39] |
| FCF definition | PAT + tax + D&A + net finance costs + impairment + unrealised FV − WC changes − IAS 7 non-cash − capex funded via permitted indebtedness − tax paid | — | [D008.1, p. 39] |
| LFCF definition | PAT + tax + D&A + net finance costs + impairment + unrealised FV − finance costs paid − tax paid − NWC − capex + borrowings proceeds − repayments | — | [D008.1, p. 39] |
| Headline earnings basis | SAICA Circular 1/2023; adj. (profit)/loss on PPE disposal, impairment/reversals, bargain purchase gain, tax effect | — | [D008.1, p. 39] |

---

### 6. Next Section to Capture

**`D008.2` (APM reconciliations, physical PDF pp. 40–47)** — this is the single most useful next section because it should contain the actual reconciliation tables (AISC, Adjusted EBITDA, net debt, FCF, LFCF, headline earnings) that will resolve the highest-priority open items: **Q118, Q119, Q120, Q121, Q122, Q123, Q34 (remainder), Q36 (remainder), Q63 (remainder), Q81 (remainder), Q86, Q87, Q89 (remainder), Q100 (remainder), Q108 (remainder), Q112 (remainder)**. If D008.2 is not available, **`D009` (Group production summary, pp. 48–50)** is the next best — it will resolve **Q2 (remainder), Q20 (remainder), Q124, Q125** and the by-mine AISC reconciliation.