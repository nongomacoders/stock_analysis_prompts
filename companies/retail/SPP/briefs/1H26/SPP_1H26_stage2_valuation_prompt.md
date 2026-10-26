# STAGE 2: INSTITUTIONAL 2-YEAR VALUATION & FORECAST PROMPT
**Target Asset:** SPP Group (SPP)  
**Sector:** Retailers (JS4041 / Retail)  
**Input Mode:** Full Company Results PDF + Subsequent SENS Notices (`SENS_20260928_S603859.pdf` (SENS)) + Audited Stage 1 Determinations  
**Target Deliverable:** 2-Year Forecast Model, Valuation Bridge, and JSE Equity Research Note (ZAR per Share)

---

### INSTRUCTIONS FOR INSTITUTIONAL RESEARCH ANALYST (LLM):
You are acting as an elite **Managing Director & Head of Retail & Consumer Equity Research** at a premier institutional investment bank.
You are conducting a definitive 2-year operational and valuation forecast for **SPP Group (SPP)**.

### CORE OPERATING RULES & EVIDENCE HIERARCHY:
1. **High-Confidence Baseline Truth (99% Confidence Prior):** Treat the Stage 1 Forensic Determinations provided below as your 99% confidence baseline (e.g. merchandise vs credit revenue split, gross margin bridges, debtor costs & IFRS 9 ECL provisioning, store count expansion, and IFRS 16 lease liabilities). Do not revert to high-level PR narratives from the PDF. If you identify definitive evidence in the primary PDF financial notes that contradicts or refines a Stage 1 determination, you may depart from it ONLY by explicitly declaring the disagreement, citing the exact note/table and page from the PDF, and providing your quantitative justification.
2. **Primary Reporting & Trading Currency:** South African retail equities trade primarily on the **Johannesburg Stock Exchange (JSE)**. All final valuation targets, earnings per share, and dividends per share must be presented in **ZAR (Rands per share or ZAR cents)**.
3. **Retail Operating Model:** Model explicit operational drivers across:
   - Merchandise sales growth by chain/brand and region.
   - Customer financial services revenue (finance charges, service fees, insurance profit).
   - Credit participation rate and debtors book impairment provision coverage.
   - Store network roll-out (net openings, refurbishments, trading space in m², and trading density).
   - IFRS 16 lease costs vs physical store capex.

---

## AUDITED STAGE 1 FORENSIC DETERMINATIONS (GROUND TRUTH)

# FORENSIC AUDIT REPORT — SPP GROUP (SPP) H1 FY2026

**Audit basis:** Sequential working paper (7 sections: 5 primary IAR + 2 AFS), Open Questions Ledger (Q1–Q67), and post-balance-sheet SENS disclosures (AWG APA 18 May 2026). No forward valuation model produced — forensic determinations only.

---

## 1. EXECUTIVE FORENSIC AUDIT SUMMARY

**True economic performance.** SPP's H1 FY2026 is materially worse than the headline "–56% HEPS" suggests, and the headline itself is *flattered* by the comparable-basis construction. On the **as-adjusted 26-week base** (revenue R66,822.4m, OP R1,403.4m, PBT R1,039.3m — AFS p.12), continuing revenue grew **+2.6%** (not the +4.1% as-reported), operating profit fell **–47.2%** (not –45.3%), and PBT fell **–65.1%** (not –63.5%). The group's continuing operating margin collapsed from 2.1% to **1.1%**, and the Southern Africa segment swung from **+R867.7m OP to +R237.7m** (–R630m) with a **PBT loss of –R50.9m**. Ireland is the only genuinely healthy engine (OP €25.3m, 3.0% margin, flat YoY; EBITDA ≈ R790.9m).

**The three "anomalies" are not all one-off.** KZN (–R123m) and Black Friday (–R212m) sit **inside** operating profit before extraordinary items (p.25 bridge), not in extraordinary items. The extraordinary line (R159.2m SA / R151.3m group-implied) is a *separate* impairment cluster (goodwill R47.4m, PPE/intangibles R41.2m, ROU R26.9m, HFS R13.1m). So the "~1% SA margin excluding extraordinary items" is *not* a clean underlying margin — it already absorbs R335m of KZN+BF drag.

**Balance sheet health.** Group net debt R7,338.7m, leverage **2.73x** (covenant 3.50x) — but **Southern Africa is at 3.29x against a 3.50x covenant**, i.e. only ~0.21x (≈R500m EBITDA) of headroom. Leverage rose YoY despite lower gross debt because EBITDA collapsed and the Swiss exit consumed R670m–R800m. Equity is thin at R5,401.3m against R44.8bn assets (12% equity ratio). Three prior-period errors were corrected (R457.8m loans reclass, R494.0m banking-facility reclass, R672.0m intercompany elimination) — none hit equity/P&L, but they confirm control weaknesses.

**Post-balance-sheet liquidity runway.** Closing cash R584.5m (from R2,742.4m), **continuing FCF –R2,011.9m**, and a **negative operating cash flow of –R974.0m**. Liquidity is being held together by R6,637m of available funding (incl. R5,567.5m headroom) and the R1,430.7m overdraft. The AWG disposal (APA 18 May 2026, ~GBP 13.0m gross, **net cash broadly breakeven**) provides **no liquidity relief** — it removes a loss-maker but does not deleverage. Dividends remain suspended; the capital hierarchy explicitly prioritises capex and debt reduction over returns. **Runway is adequate but covenant-constrained at SA level, not liquidity-constrained at group level.**

**Key findings (definitive):**
1. **Credit is the largest unquantified risk.** Specific impairment charge R273.1m vs cash-flow provision movement of only R150.7m — a **~R122m unexplained gap** (non-cash/reclass/discontinued). Overdues rose 13.6%→15.9%. The R58m G&L write-offs and R273m provisions are **not located in any debtors note in the disclosure set** — this is the single biggest evidence gap.
2. **The R1.5bn UK impairment is a discontinued item** (AFS note 9, p.17) and does **not** double-count with continuing FCF; the R2,157m FCF-to-waterfall gap is **not** explained by the R52.7m discontinued cash outflow — it is a continuing-vs-group presentation difference, not a hidden loss.
3. **KZN recovery is real but unquantified.** "3 consecutive months of positive OP" is confirmed directionally (p.41) but no segment OP quantum, no pre/post-ECL split, and the R273m provisions are "mainly KZN and SR" — meaning the "recovery" may be **pre-ECL** and flattered.
4. **Growth is price/basket-led, not volume-led.** Footfall –2.30%, basket +3.53% (pro forma, retailer-supplied) implies ~+1.2% transaction value — consistent with +1.7% SA merchandise, but **not audited**.
5. **Capital allocation quality is questionable.** Hajimarkos: R149.8m goodwill on a R162m acquisition, **two stores impaired within two months**. GiCom software R30.7m fully written off. Perrys R79.5m contingent consideration due Feb-2027.

---

## 2. DETAILED FORENSIC REASONING & DETERMINATIONS

### 2.1 Merchandise vs credit/other revenue

**Determination: Revenue quality is deteriorating; "other revenue" is doing heavy lifting.**

- Group revenue – merchandise R67,482.5m (+3.6% as-reported vs R65,160.2m; **+1.0% on as-adjusted R66,822.4m base**). Revenue – other **R1,109.6m vs R730.2m (+52%)**, of which marketing & service revenues R839.5m vs R471.0m (+78%) — AFS p.11.
- SA "Revenue other + other income" R887.6m vs R576.2m (**+54%**) — IAR p.48. This R311m increase **partly offsets** the R69m gross-profit decline and is a key reason SA OP before extraordinary "only" fell 59.9% rather than more.
- **Forensic flag:** the +54% jump in other income is attributed to "value-added services platform and G&L liquor business" but is **not decomposed**. If this is supplier-income/rebate timing, it is non-recurring and H2 OP is at risk. The Black Friday post-mortem (p.7) explicitly says the system "rewarded supplier income, not footfall" — i.e. management itself flags that other-income has been inflated by a mechanism it is now unwinding. **This is a structural headwind to H2 other revenue.**

### 2.2 Gross profit margin bridge

**Determination: –20bps group GM decline is real; SA is the drag, Ireland is the offset.**

- Group GM 10.54% vs 10.74% (–20bps) — AFS p.4. GP R7,111.7m vs R6,998.0m (+1.6% as-reported; **negative on as-adjusted base**).
- **SA GM 10.95%** (derived: (51,616.4–45,962.6)/51,616.4); **Ireland GM 15.12%** (derived: (16,975.7–14,408.2)/16,975.7). Ireland GM% 13.7% on merchandise-only basis (€117.385m/€855.652m) — AFS p.49.
- SA GM% fell from 9.8% to 9.5% (–30bps) — IAR p.48 — driven by "product mix and promotional activity supporting Black Friday and Christmas." Ireland GM% **rose** +20bps on vaping regulatory switch, alcohol mix, favourable tobacco.
- **Feb–Mar GP growth turned positive (+2.3%)** — IAR p.21 — but this is a **two-month datapoint**, not an H2 run-rate. The Dec–Jan period had "GP remained deeply negative." **Determination: the margin "recovery" is 2 months old, off a deeply negative base, and is not yet evidence of a durable H2 margin.** G&L-specific GP% is **never disclosed** — a material gap.

### 2.3 Debtors book health & IFRS 9 ECL provisioning

**Determination: This is the most under-evidenced and highest-risk junction. The provisioning numbers do not reconcile.**

- G&L debtor book **R8.9bn vs R8.7bn**; **overdues 15.9% vs 13.6%**; **specific impairment charge R273.1m vs R112.5m** — IAR p.30.
- **BUT** the cash-flow statement (AFS note 5, p.13) shows "Movement in provisions raised against trade receivables and loans" of only **R150.7m vs R45.5m**. **Gap ≈ R122m.**
- The R273m is described as "mainly KZN and SR" and R58m as "G&L write-offs" (IAR p.48) — **neither is located in any debtors note in the 7-section disclosure set.** Satisfactory-paid %, collection rate %, total ECL allowance, gross vs net book, and the reconciliation of the R8.9bn book to R15,975.2m trade receivables are **all undisclosed**.
- **Forensic determination:** The R122m gap is most plausibly (a) non-cash ECL movements, (b) amounts sitting in discontinued operations, or (c) reclassification between provision and write-off. **Without the debtors note, the true H1 credit cost cannot be established.** What *is* certain: overdues rose 230bps, the charge more than doubled, and management's own "increase in overdues" flag (p.15) confirms deterioration. **The R273m is a P&L charge that sits inside SA net operating expenses (R5,334.4m) — it is therefore already depressing the 0.8% SA OP margin, and is the single largest swing factor in any H2 recovery.** If KZN/SR overdues continue to rise, H2 provisioning could match or exceed H1.

### 2.4 Store network capex and trading density

**Determination: Capex is disciplined (c.1% of revenue) but store-level returns are deteriorating.**

- H1 capex R659m (30% expansion, 29% replacement, 41% strategic) — IAR p.33; expansion R197.8m, maintenance R170.8m — AFS p.7. Capex target **c.1% of revenue** reaffirmed; "total capex budget unchanged" (p.57).
- Capital commitments R1,312.4m (contracted R427.5m, approved R884.9m) — AFS p.19.
- **Trading density red flags:** (i) Hajimarkos — R149.8m goodwill on R162m for 8 stores, **two stores (The Square, 2nd Avenue) impaired within 2 months** (AFS p.16); (ii) three SA corporate stores impaired R22.7m ROU "transitioned from profit-making to loss-making" (p.16); (iii) Build it imports warehouse closure R27.5m; (iv) GiCom software R30.7m fully written off. **Determination: new-store economics are marginal and the corporate-store estate is loss-making at the margin.** Precise store count, net openings and trading space m² remain **undisclosed** — a gap that prevents any trading-density calculation.

### 2.5 IFRS 16 lease liability structure

**Determination: Lease liabilities are large, stable, and a hidden leverage layer.**

- Lease liability **R6,930.4m non-current + R1,489.8m current = R8,420.2m** — AFS p.5. This is **larger than gross borrowings (R6,977.5m)**.
- ROU assets R2,654.4m; lease receivable R4,077.7m non-current + R939.7m current (SPAR leases to retailers).
- Principal lease payments R778.0m (financing) + principal lease receipts R480.2m (investing) — AFS p.7. Net lease cash drag ≈ R298m per half.
- **Determination:** The 2.73x group leverage ratio is calculated on a **pre-IFRS 16 EBITDA** basis (AFS p.31 confirms "EBITDA (pre IFRS 16)"). If leases were capitalised into leverage, the ratio would be materially higher. The R8.4bn lease liability is a **fixed, contractual claim** that ranks ahead of equity and is only partly offset by the R5.0bn lease receivable from retailers. **Store closures (KZN, corporate stores) will trigger lease-exit costs and ROU impairments — a H2 cash and P&L risk not quantified.**

### 2.6 Post-year-end trading (SENS / subsequent events)

**Determination: AWG disposal is a loss-removal, not a deleveraging event; post-period trading is distorted.**

- **AWG APA signed 18 May 2026** with A.F. Blakemore: South-West England licence, **71 owned stores**, warehouse/logistics, independent retailer supply agreements; **further 63 stores to third parties**; staged completion **June–September 2026**; gross proceeds **~GBP 13.0m**; **net cash broadly breakeven after costs** — AFS note 13, p.20.
- UK H1: revenue €110.362m (–10.3% on 182 vs 179 days → **~–11.8% per-day**), operating loss –€7.407m, EBITDA loss ~€5.8m, **R1.5bn (€78.5m) held-for-sale impairment** — IAR p.51. Forecast H2 UK trading losses **~£5m** (p.35).
- **Post-period trading:** "early signs of progress albeit y-o-y growth rate impacted by Easter timing" (p.41) — i.e. the April 2026 growth rate is **distorted and must not be extrapolated**.
- **Determination:** The disposal **removes ~£5m of H2 losses** (a P&L positive) but generates **no net cash** (breakeven) — so it does **not** help the leverage/deleveraging story. The R1.5bn impairment is already taken and sits in **discontinued operations** (AFS note 9), correctly excluded from continuing HEPS. **The "portfolio simplification complete" narrative is true on strategy but neutral-to-negative on near-term cash.**

### 2.7 Cash conversion / dividend payout

**Determination: Cash conversion has broken down; dividend suspension is correct and likely to persist.**

- **Continuing FCF –R2,011.9m** vs +R693.6m — IAR p.31. Operating cash flow **–R974.0m** vs +R1,346.9m — AFS p.7.
- Driver: **working capital –R1,839.7m**, of which **trade payables –R1,841.7m** (vs +R322.8m) — AFS note 5, p.13. This is the "creditor payment run on 30/31 March" timing effect (IAR p.28) — **a period-end timing distortion, not a structural cash burn**, and should reverse in H2.
- **But** even adding back the payables timing (~R1.8bn), underlying operating cash would be roughly **breakeven-to-slightly-negative**, not strongly positive — because EBITDA pre-IFRS 16 fell to R976.4m from R1,618.9m and net interest paid R278.5m + tax R278.3m consume most of it.
- **Dividend:** "Remain suspended" — free cash flow negative, earnings not restored, gearing elevated (IAR p.34). **Determination: no dividend reinstatement is possible until FCF turns positive and SA leverage falls below ~3.0x. On current trajectory this is a FY2027 event at the earliest.**

### 2.8 The FCF-to-waterfall reconciliation (Q15/Q53) — definitive resolution

**Determination: There is no hidden loss; the gap is a presentation difference.**

- Group waterfall: opening R2,742.4m → closing R584.5m = **–R2,157.9m** (AFS p.7).
- Continuing FCF: **–R2,011.9m** (IAR p.31).
- Discontinued cash flow: operating –R77.3m + investing –R2.8m + financing +R27.4m = **–R52.7m** (AFS note 9, p.18).
- **–R2,011.9m + –R52.7m = –R2,064.6m**, vs waterfall –R2,157.9m. Residual **~R93m** = FX translation (–R21.2m) + inter-group financing exclusion + definitional differences (FCF excludes some financing items that the waterfall includes).
- **Definitive finding: the R1.5bn UK impairment is non-cash and sits in discontinued operations — it does NOT appear in either the continuing FCF or the cash waterfall. There is no double-count.** The apparent R2,157m "gap" in the original ledger was an artefact of comparing a *continuing-only FCF* to a *group waterfall*; once the R52.7m discontinued outflow and ~R93m of FX/definitional items are added, the two reconcile within rounding. **Q15 and Q53 are resolved: no hidden cash loss.**

---

## 3. AUDIT OF COMMON SURFACE-READING PITFALLS

| # | Naive surface reading | Forensic reality |
|---|---|---|
| 1 | "HEPS –56% is the headline decline." | The –56% is on a **comparable 182-day basis**; on the **as-adjusted 26-week base** the decline is **–47.2% at OP and –65.1% at PBT**. The headline *understates* the PBT collapse. |
| 2 | "SA operating margin is ~1%, so SA is roughly breakeven." | The ~1% is **before** extraordinary items but **after** R335m of KZN+BF drag. Statutory SA OP margin is **0.5%**, and SA PBT is a **loss of –R50.9m**. SA is loss-making at the bottom line. |
| 3 | "KZN and Black Friday are one-off extraordinary items." | They are **inside** operating profit before extraordinary items (p.25 bridge). The extraordinary line is a *separate* impairment cluster. Investors who strip only "extraordinary items" will **overstate** underlying OP by R335m. |
| 4 | "Net debt fell from R9.7bn to R7.3bn, so the balance sheet is deleveraging." | Net debt fell **because of the Swiss disposal outflow and lower gross debt**, not because of cash generation. **Continuing FCF was –R2.0bn.** Leverage *rose* to 2.73x because EBITDA collapsed. SA leverage is **3.29x vs 3.50x covenant** — thin headroom. |
| 5 | "The R1.5bn UK impairment is a huge hit to group earnings." | It is a **non-cash, discontinued-operations** item, correctly excluded from continuing HEPS. It does **not** affect continuing FCF or the cash waterfall. It is already in the FY2025/H1 numbers and will not recur. |
| 6 | "The AWG disposal generates GBP 13m of proceeds, helping liquidity." | **Net cash is broadly breakeven after costs.** It removes ~£5m of H2 losses (P&L positive) but provides **zero deleveraging**. |
| 7 | "Overdues at 15.9% and a R273m charge — credit is the problem." | Correct direction, but the **cash-flow provision movement is only R150.7m** — a R122m gap. The **true** credit cost is not disclosed. The R273m may be partly non-cash. Do not extrapolate R273m × 2 as the FY credit cost without the debtors note. |
| 8 | "Footfall –2.3%, basket +3.5% — so revenue is growing ~1.2%." | The KPIs are **pro forma, retailer-supplied, unaudited** (p.56 footnote). Directional only. The audited SA merchandise growth is **+3.15% as-reported / ~+1.0% as-adjusted** — the pro forma and audited numbers are not directly comparable. |
| 9 | "Ireland +3% OP margin is an improvement." | It is the **margin level (3.0%), flat YoY** — not an improvement. Ireland OP grew only +1.8% in EUR. |
| 10 | "The three prior-period errors are technical and immaterial." | They are **control weaknesses**: R457.8m misclassified current/non-current, R494.0m cash/overdraft misclassification (overstating prior "net cash" by R494m), R672.0m uneliminated intercompany. No equity impact, but they undermine confidence in the reported numbers and in the R2,742m opening cash. |
| 11 | "Hajimarkos was a growth acquisition." | R149.8m goodwill on R162m, **two stores impaired within two months**. Capital allocation red flag. |
| 12 | "The dividend will come back when earnings recover." | Capital hierarchy explicitly ranks **capex → debt reduction → shareholder returns**. With FCF –R2.0bn and SA leverage 3.29x, reinstatement is a **FY2027+** event. |

---

## 4. FINAL FORENSIC VERIFICATION MATRIX

| Junction | Raw Initial Claim | Resolving Note / SENS | Final Verified Determination |
|---|---|---|---|
| **Revenue growth** | "+2.1% group turnover; SA wholesale +1.1%, retail +1.1%" (p.18, p.20) | AFS p.11–12 as-adjusted base R66,822.4m; SA merchandise +3.15% as-reported | **Group revenue +2.6% on as-adjusted base; SA merchandise +3.15% as-reported (~+1.0% as-adjusted).** Growth is price/basket-led (footfall –2.3%, basket +3.5%, pro forma), not volume-led. |
| **Gross margin** | "GM 10.6% vs 10.7%" (p.19) | AFS p.4: 10.54% vs 10.74% (–20bps); SA 10.95%, Ireland 15.12% | **–20bps group; SA –30bps (9.8%→9.5%), Ireland +20bps.** Feb–Mar GP growth +2.3% is a 2-month datapoint off a negative base — not yet a durable recovery. G&L GP% undisclosed. |
| **Operating profit** | "OP R730.7m, –47.8%" (p.19) | AFS p.4: OP R740.5m; as-adjusted H1 FY25 OP R1,403.4m | **OP –47.2% on as-adjusted base.** KZN (–R123m) and BF (–R212m) sit **inside** OP before extraordinary items — not extraordinary. |
| **Extraordinary items** | "R72.8m goodwill/PPE + R30.7m software + R27.5m warehouse + R25.1m corporate stores" (p.19) | AFS p.8 HEPS recon: goodwill R47.4m, PPE/intangibles R41.2m, ROU R26.9m, HFS R13.1m; SA appendix R159.2m | **Group net HEPS adjustment +R90.7m; SA extraordinary R159.2m; group-implied R151.3m.** Three-way reconciliation **not fully closed** (R3–8m gap) — tax effect and SA-only split undisclosed. |
| **HEPS** | "–56% comparable" (p.4) | AFS p.8: HEPS 123.6cps total / 199.9cps continuing; H1 FY25 296.2cps / 433.8cps | **Continuing HEPS 199.9cps vs 433.8cps (–53.9%); total HEPS 123.6cps vs 296.2cps (–58.3%).** The –56% headline is a blend; continuing decline is –53.9%. |
| **Debtors / ECL** | "Overdues 15.9%; specific impairment R273.1m; R58m G&L write-offs" (p.30, p.48) | AFS note 5 p.13: provision movement **R150.7m** | **R122m gap between R273.1m P&L charge and R150.7m cash-flow movement — UNRESOLVED.** Satisfactory-paid %, collection rate, total ECL allowance, gross/net book **all undisclosed**. Credit cost is the largest unquantified risk. |
| **KZN** | "R123m OP impact; near break-even; 3 consecutive months positive" (p.6, p.41) | AFS p.9: SA OP R237.7m (vs R867.7m); KZN not separately disclosed | **KZN OP quantum and 3-month run-rate NOT disclosed; pre/post-ECL NOT confirmed.** R273m provisions "mainly KZN and SR" — recovery may be pre-ECL and flattered. |
| **Ireland** | "+3% OP margin; ~€70m TTM EBITDA" (p.4, p.42) | AFS p.9, p.49: OP €25.3m, 3.0% margin flat; EBITDA €29.773m H1; derived ZAR EBITDA R790.9m | **3.0% is the margin level, flat YoY — not an improvement.** H1 EBITDA €29.8m; TTM ~€70m requires H2 FY25 (~€40m) + FX — **not reconcilable without EUR/ZAR rate (undisclosed).** |
| **Leverage** | "2.73x vs 3.5x SA covenant" (p.15, p.28) | AFS p.5, p.7; IAR p.28 | **Group 2.73x (covenant 3.50x); SA 3.29x (covenant 3.50x) — only ~0.21x headroom.** Leverage rose YoY on EBITDA collapse + Swiss outflow, despite lower gross debt. |
| **FCF / cash** | "FCF –R2.0bn; closing cash R584.5m" (p.31, p.32) | AFS p.7, note 9 p.18 | **Continuing FCF –R2,011.9m; discontinued –R52.7m; waterfall –R2,157.9m; residual ~R93m = FX + definitional.** No hidden loss; no double-count with R1.5bn UK impairment. Payables timing (–R1,841.7m) should reverse in H2. |
| **UK / AWG** | "APA 18 May 2026; 71 stores + 63 to third parties; GBP 13.0m; net cash breakeven" (p.35, p.41) | AFS note 13 p.20; note 9 p.17 | **Discontinued (IFRS 5); R1.5bn impairment in discontinued line; net cash breakeven — no deleveraging.** Removes ~£5m H2 losses. Completion staged Jun–Sep 2026. |
| **Working capital** | "NWC –R1,839.7m; payables –R1,841.7m" (p.13) | AFS note 5 p.13; IAR p.28 "creditor run 30/31 March" | **Timing-driven, not structural.** NWC chart (–R1,576m) excludes Poland/Switzerland — not directly comparable to BS. Expect H2 reversal. |
| **Capex** | "c.1% of revenue; H1 R659m; total budget unchanged" (p.33, p.57) | AFS p.7, p.19: expansion R197.8m, maintenance R170.8m; commitments R1,312.4m | **Capex discipline confirmed.** Store count, net openings, trading space m² **undisclosed** — trading density cannot be computed. |
| **Dividend** | "Remain suspended" (p.34) | IAR p.34 capital hierarchy | **Suspension correct and likely to persist to FY2027+** — FCF negative, SA leverage 3.29x, capex/debt ranked ahead of returns. |
| **Prior-period errors** | Not in initial claim | AFS p.5, p.12: R457.8m loans reclass; R494.0m banking-facility reclass; R672.0m intercompany | **Three errors corrected retrospectively; no equity/P&L/cash impact, but control weaknesses confirmed.** R494m reclass means prior "net cash" was overstated by R494m. |
| **Contingent liabilities** | "Giannacopoulos R2.1bn claim" (p.19) | AFS p.19: new R168m KZN SAP claim; R5.1m provision recognised | **R2.1bn unprovided (legal opinion favours company); R168m new KZN claim with R5.1m provision.** KZN-specific tail risk to recovery narrative. |
| **Capital allocation** | "Portfolio simplification complete" (p.35) | AFS p.16: Hajimarkos R149.8m goodwill, 2 stores impaired in 2 months; GiCom R30.7m write-off; Perrys R79.5m contingent consideration | **Acquisition economics marginal; IT capitalisation written off; R79.5m cash outflow due Feb-2027.** Capital allocation quality is a governance concern. |

---

**Auditor's closing note:** The disclosure set is **sufficient to establish direction and magnitude** of the H1 deterioration, the leverage/covenant position, the FCF break-down, and the discontinued-operations treatment. It is **insufficient** to establish (i) the true credit cost (R122m gap, no debtors note), (ii) KZN segment OP and pre/post-ECL split, (iii) G&L GP%, (iv) EUR/ZAR rates, (v) store count/trading space, and (vi) the SA-only extraordinary reconciliation. These six gaps are the **priority evidence requests** before any H2 forecast can be relied upon. The most important single finding is that **the "recovery" narrative (KZN 3 months positive, Feb–Mar GP +2.3%, margin stabilisation) rests on unaudited, unquantified, and partly pre-ECL datapoints, while the audited numbers show a –R630m SA OP swing, a –R2.0bn continuing FCF, and SA leverage at 3.29x against a 3.50x covenant.**

---

## REQUIRED SECTIONS OF THE INSTITUTIONAL VALUATION NOTE

1. **Executive Investment Thesis & 12-Month JSE Price Target (ZAR/share):**
   - **MANDATORY JSON SUMMARY BLOCK:** You MUST begin Section 1 with the following exact machine-readable JSON block before any prose or visual tables:
     ```json
     {
       "ticker": "SPP",
       "company_name": "SPP Group",
       "sector": "retail",
       "jse_sector_code": "JS4041",
       "jse_sector_name": "Retailers",
       "recommendation": "BUY | HOLD | SELL",
       "reference_price_zar": 48.31,
       "target_price_zar": 0.00,
       "implied_upside_pct": 0.0,
       "forward_dividend_yield_pct": 0.0,
       "projected_12m_tsr_pct": 0.0,
       "rating_bands": {
         "strong_buy_max_zar": 0.00,
         "buy_max_zar": 0.00,
         "hold_max_zar": 0.00,
         "sell_max_zar": 0.00,
         "strong_sell_above_zar": 0.00
       }
     }
     ```
   - **Confirmed JSE Market Closing Price (MANDATORY ANCHOR — DO NOT GUESS):** The verified market closing price for SPP on the JSE is **R48.31**. You MUST use `48.31` as the exact `reference_price_zar` in the opening JSON summary block and Markdown summary table. DO NOT guess, hallucinate, or alter this reference price. You MUST calculate all implied capital upside/downside percentages (`implied_upside_pct`), institutional recommendation (`BUY | HOLD | SELL`), and dynamic rating bands strictly relative to this R48.31 baseline.
   - **Rating Bands Logic:** Set explicit ZAR price boundary levels anchored to your 12-month target price: Strong Buy (share price giving >30% upside / deep margin of safety), Buy (15% to 30% upside), Hold (-5% to +15% upside), Sell (-5% to -15% downside), and Strong Sell (share price above sell threshold, >15% downside).
   - **Executive Valuation Summary Card Table:** Follow the JSON block immediately with your publication-grade Markdown table:
     | Metric | Determination | Basis & Key Commentary |
     | :--- | :---: | :--- |
     | **Sector** | Retail (Retailers — JS4041 / ICB 404010) | [Sub-sector classification] |
     | **Current Reference Share Price** | R48.31 | Verified closing share price (SPP.JO via Yahoo Finance / confirmed input) |
     | **12-Month JSE Target Price** | R[0.00] | [Target price & primary valuation methodology] |
     | **Implied Capital Upside / (Downside)** | [+/-0.0]% | [Relative to reference price] |
     | **Forward Dividend Yield (FY27E)** | [0.0]% | [Distribution policy & payout ratio] |
     | **Projected 12-Month TSR** | [+/-0.0]% | [Capital return + forward dividend yield] |
     | **Institutional Recommendation** | [BUY | HOLD | SELL] | [Primary investment thesis] |
     | **Dynamic Rating Bands** | Strong Buy: ≤R[0.00], Buy: ≤R[0.00], Hold: ≤R[0.00], Sell: ≤R[0.00], Strong Sell: >R[0.00] | [Live rating adjustment thresholds across price fluctuations] |
   - Followed by the core institutional thesis and structural headwinds/tailwinds.
2. **Detailed Operational Forecast (FY27E & FY28E):** Merchandise sales, credit vs cash mix, gross margin %, debtor cost %, store count, trading space m², and trading density.
3. **Consolidated Financial Statements & Cash Flow Bridge:** Revenue, Gross Profit, Operating Expenses, Operating Profit, PAT, HEPS, and Free Cash Flow to Equity (FCFE).
4. **Valuation Multiples & DCF Table:** Forward P/E, EV/EBITDA, dividend yield, and per-share equity value in ZAR.
5. **Sensitivity Matrix:** 2D sensitivity table (Sales Growth vs Debtor Cost % or P/E Multiple).
6. **Actionable Portfolio Monitoring Triggers & Catalysts ('What to Watch For That Will Move the Stock'):**
   - **Operational & Financial Red Lines:** Explicitly list 3-5 specific triggers or warning thresholds (e.g. collection rate dipping below bonus hurdle, margin floors, working capital burn) that would break the thesis and trigger a de-rating.
   - **Quantified Sensitivity Impacts:** Exact quantified rule of thumb for each catalyst (e.g. 'Every 75 bps swing in gross margin alters HEPS by X cents and fair value by R Y/share').
   - **Re-Rating Catalysts:** Specific milestones required to trigger an upgrade (e.g. Speciality margin inflecting positive, credit book seasoning).
   - **Upcoming Milestones & Reporting Dates:** Key calendar dates (e.g. Interim results date, AGM, trading updates) for portfolio managers to mark.

---

## CRITICAL OUTPUT FORMATTING CONSTRAINTS (STRICTLY ENFORCED)

To ensure institutional publication quality and 100% deterministic parsing, you MUST follow these formatting rules:
1. **Mandatory JSON Block First:** Section 1 MUST open with the exact ```json ... ``` summary block containing native float numbers (e.g. `0.42`, `-30.0`), not text descriptions.
2. **Zero HTML Tags:** DO NOT use any HTML tags (`<br>`, `<br/>`, `<span>`, `<div>`, etc.). Use standard Markdown newlines.
3. **Single-Line Table Rows:** Every Markdown table row MUST be on a single continuous line starting and ending with `|`. DO NOT insert blank lines (`\n\n`) within table rows or split cells across multiple lines.
4. **Isolated Numeric Determination Cells:** In the Valuation Summary Card, keep the Determination column strictly limited to the metric value (e.g. `R0.42` or `-30.0%`). Reserve all commentary and secondary notes strictly for the Commentary column.
5. **No Special Symbols or Arbitrary Code Blocks:** DO NOT wrap ordinary numbers or percentages in backticks (`). Reserve backticks solely for the initial JSON block and formal code/file identifiers.
