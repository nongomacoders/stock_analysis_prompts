# FORENSIC AUDIT REPORT — TKG RESOURCES (TKG) FY2026

---

## 1. FORENSIC AUDIT SUMMARY

**Verdict: The reported earnings recovery is real but materially overstated by non-recurring items; the balance sheet is genuinely de-risked; the cash flow story is weaker than the headline FCF suggests; and the "no impairment" outcome rests almost entirely on a 580bps discount-rate cut at BCX.**

**True economic performance.** Group revenue grew only **+1.4% to R44,477m**, but EBITDA rose **+5.8% to R12,480m** (margin 28.1%, +1.2ppts) — the entire improvement is cost-driven, not revenue-driven. The revenue mix is structurally deteriorating at the legacy end (fixed voice −21.8%, CPE −23.0%, non-fibre data −33.4%) and being replaced by data (+9.1% data-led, mobile data +10.5%). **The reported +21.5% HEPS growth is against a pro-forma FY2025 base of 583.2c that itself was flattered by a R4,408m Swiftnet disposal gain and a R618m TRF settlement loss.** On a clean continuing basis, HEPS of 708.5c is a genuine improvement, but the quality is mixed: it includes a **R209m contract-asset factoring gain** and a **R194m PP&E disposal gain** that management does *not* adjust for.

**Balance sheet health.** Genuinely strong. Interest-bearing debt fell **−43% to R6,593m**; cash of R7,723m means the Group is in a **net cash position of R1,130m excluding leases** (net debt R6,426m including R7,556m lease liabilities). Net debt/EBITDA is **0.5x including leases, −0.1x excluding** — comfortably inside the 3:1 covenant. **But the leverage metric is defined ex-lease and EBITDA is grossed up by interest income** — both flatter the ratio.

**Post-balance-sheet liquidity runway.** Ample. Committed undrawn facilities of **R5,672m** plus cash of R7,723m give a committed liquidity buffer of **~R13.4bn** against R2,069m of current debt maturities. The FY2026 dividend of **R1,381m (270.10cps)** was declared 29 May 2026 and is payable from this position. **However, the R1,381m dividend is 45% of a FCF figure (R3,068m) that itself includes a R240m non-recurring cell-captive dividend and R209m of factoring gains** — clean FCF is closer to R2,600–2,800m, implying a true payout nearer 50–53%.

**Key findings (ranked by severity):**
1. **BCX "no impairment" is a discount-rate artefact.** The BCX pre-tax discount rate fell from **20.8% to 15.0%** (−580bps) — the sole reason R1,295m of goodwill survives. Consumer and Openserve breakeven sensitivities are tight (17.6%/2.6% and 17.1%/2.2% respectively).
2. **FCF quality is overstated.** Headline FCF +10.4% to R3,068m includes R240m cell-captive dividend (new) and R209m factoring gain; clean FCF growth is ~+1.8%.
3. **Cash tax collapsed −92%** (R396m→R32m) on assessed-loss utilisation — a trough year that will normalise upward, compressing future FCF.
4. **The R4,408m Swiftnet gain (P&L) vs R1,164m (§12.2) reconciliation gap of R1,244m remains unexplained** — the single largest unresolved arithmetic item.
5. **Revenue quality:** the "three years and two quarters of market-leading mobile service revenue growth" claim is supported by +6.8% mobile service revenue, but BCX revenue fell −8.6% and cybersecurity revenue fell −5.5% *contradicting* the GCEO's "growing robustly" claim.

---

## 2. DETAILED FORENSIC REASONING & DETERMINATIONS

### 2.1 Service Revenue vs Device Financing (IFRS 15)

**Determination: Device financing is correctly separated, but the "over-time" revenue subtotal is contaminated by interest accretion and must be stripped for clean service-revenue forecasting.**

- Revenue disaggregation (p.36) shows **R38,336m recognised over time** and **R5,548m at a point in time**. Footnote [^2] confirms the over-time subtotal **includes R434m of customer interest revenue** (the IFRS 15 significant financing component on CPE/device bundles). Clean over-time service revenue = **R37,902m**.
- The **CPE restatement** (footnote [^1], p.36): R700m was reclassified from point-in-time to over-time in the prior year — a disclosure-only correction with no P&L impact. Arithmetic reconciles (3,619+700=4,319; 784−700=84).
- **Google Equiano** (p.29): Openserve received a 15-year upfront payment with a **USD-denominated significant financing element**, accreted through finance cost and deferred revenue over 15 years. This is a long-tail, USD-linked deferred revenue balance (part of the R3,101m deferred revenue) that accretes at a USD rate — an embedded FX exposure inside a ZAR reporter.
- **Principal-vs-agent:** BCX software/cloud is largely **agent (net)**; integrated solutions are **principal (gross)**; non-ceded Enterprise contracts (R3,801m, down −15.5%) remain **principal at Telkom** and are a structural run-off line.

**Forensic conclusion:** Model service revenue ex-interest (R37,902m base), treat the R434m accretion as a separate contract-term-driven line, and model the R3,801m non-ceded enterprise book as a declining run-off.

### 2.2 ARPU Trajectory & Subscriber Churn

**Determination: Subscriber growth is real but ARPU is flat-to-declining and the two fibre subscriber figures in the report are irreconcilable — a material definitional inconsistency.**

- Mobile data subscribers **19,961,588 (+31.1%)**, 77.8% of a ~25.7m base; blended ARPU **R76** (flat). Mobile data traffic **+18.5% to 2,084 PB** vs mobile data revenue **+10.5%** → implied **~6.7% price/MB deflation**.
- **Material contradiction:** p.29 states "Fibre broadband subscribers in Telkom Consumer (11.6% growth to 597,582)" while p.37 shows "Fibre broadband subscribers in Telkom Consumer 219,928 (−0.3%)". Two different figures for the same metric in the same report — **unresolved (N1)**.
- **Churn signals:** ongoing-commission contract cancellations nearly doubled (R82m→R165m); written-off-but-enforced receivables jumped **+64%** (R515m→R847m); trade receivable loss allowance rate *rose* to 38.9% despite the "stringent vetting" narrative.
- **Cybersecurity revenue fell −5.5%** (R469m→R443m) — directly contradicting the GCEO's "cybersecurity revenue growing robustly" (p.18). **Material contradiction (N4).**

**Determination:** Model mobile data revenue growth below traffic growth (price deflation persists); treat the fibre subscriber base as ~220k (the p.37 figure, consistent with the 817,540 fibre access connections and 53.1% connectivity rate on 1,539,209 homes passed); treat the 597,582 figure as a broader/different definition requiring reconciliation.

### 2.3 Tower Lease Commitments & IFRS 16 Liabilities

**Determination: Lease liabilities are growing (+9.2% to R7,556m) and are the dominant driver of reported net debt; the FY2026 remeasurement of R1,417m is CPI/indexation-driven and structural, not one-off.**

- Lease liabilities: non-current R5,357m + current R2,199m = **R7,556m** (FY2025: R6,920m). ROU assets R6,871m.
- **Remeasurements R1,417m** (FY2025: R627m) — footnote [^1] confirms these are **CPI escalations and lease modifications/renewals**. This is a **structural inflation pass-through** into the lease liability, driving finance charges up **+19% to R630m** even as debt interest fell.
- **Swiftnet externalisation:** post-disposal, tower leases are now external (TowerCo BidCo) for a full year — a structural step-up in lease cash costs. The R972m FY2025 "transfers" line confirms the internal→external reclassification.
- **Lease principal repaid R1,910m** (FY2025: R2,496m) — the FY2025 figure contained a once-off Google fibre-pair advance payment; **R1,910m is the better forward run-rate** but now includes full-year Swiftnet external leases.
- **Undisclosed renewal tail:** p.69 states renewal options on network equipment/property are **not** in the lease liability because "rental payments escalate, therefore a reasonable estimate cannot be determined" — an off-balance-sheet tail risk.
- **Committed-not-commenced leases jumped R10m→R359m** (renewals from 1 April 2026) — a FY2027 lease liability step-up.

**Guardrail compliance (`TELCOS-IFRS16-TOWER-SPECTRUM-FCF`):** Lease principal (R1,910m) and lease interest (R630m) are treated as **ongoing cash outflows** in FCFE. Cash conversion = (EBITDA 12,480 − Capex 6,295 − Lease principal 1,910) ÷ EBITDA = **34.3%** — low, and the correct basis for FCFE.

**Guardrail compliance (`ALL-IFRS16-EV-BRIDGE`):** The company's own leverage metric is **ex-lease** (net debt R(1,190)m ex-lease vs R6,426m incl. lease). Any EV-to-equity bridge must state basis explicitly: if using post-IFRS 16 EBITDA (which is after lease depreciation/interest), lease liabilities may be subtracted; if using pre-IFRS 16 EBITDA (before lease costs), they must not be double-counted.

### 2.4 Spectrum Auction Capex vs Network Modernisation Capex

**Determination: No spectrum licence cost, amortisation schedule, or rollout obligation is disclosed anywhere in the 90-section AFS — a material disclosure gap for a telco.**

- Total mobile spectrum portfolio **184 MHz** disclosed (p.29) with **no cost, no amortisation period, no remaining life, no coverage obligations**.
- Intangible assets (R5,627m) comprise goodwill R1,295m, trademarks R1,740m, software R2,252m, under-construction R340m — **no spectrum line item**. Spectrum is either embedded in an undisclosed class or sits in PP&E.
- Capex R6,434m (+10.4%), intensity **14.5%** (top of 12–15% guidance). Composition: mobile 38%, fibre 28%, POTN core 14%, IT 13%, other 7%. **Maintenance capex only R789m** vs expansion R4,837m — maintenance is low relative to depreciation of R3,609m (potential under-investment signal).
- **Authorised-uncontracted capex jumped +118% to R8,544m** while contracted fell −66% to R1,204m (three-year mobile project complete) — a forward capex acceleration signal with high timing uncertainty.

**Determination:** Separate one-off spectrum outlays (undisclosed — flag as a gap) from recurring network modernisation capex. Model FY2027 capex intensity at 13.5–14.5% given the authorised pipeline, but flag that the R8,544m uncontracted envelope is discretionary.

### 2.5 Foreign Exchange Remeasurement & Hyperinflation Adjustments

**Determination: FX is a live, growing drag; no hyperinflationary subsidiary is evidenced; all debt is local (ZAR), so FX risk sits in derivatives and procurement, not borrowings.**

- **FX & fair value movements: R(227)m** (FY2025: R(58)m) — a R169m deterioration. Fair value adjustments **R(372)m** on FX forwards (rand strengthened vs USD against hedged positions); FX gain R145m. **Directional mismatch flagged:** a strengthening rand produced a translation *gain* but a derivative *loss* — the hedge book was positioned for a weaker rand.
- **Net FX monetary liabilities widened** to ~R1,586m (USD short dominant) from ~R1,274m; **FX sensitivity ±10% = ±R116m Group / ±R250m Company** (Company anomaly: larger sensitivity on smaller net exposure — unresolved).
- **All interest-bearing debt is "local" (ZAR)** — no foreign-currency borrowings. FX exposure is in FECs (R4,488m purchased notional), procurement, and the Equiano USD accretion.
- **No IAS 29 hyperinflationary subsidiary** is referenced; functional currencies "unchanged" (p.25). BCX foreign subsidiaries "not material" (segment footnote).
- **JIBAR→ZARONIA transition:** R6,593m of debt and the FEC book are JIBAR-linked; cutover by 31 Dec 2026; management asserts "no material impact" but gives **no sensitivity** for the IFRS 16 IBR / employee-benefit swap-curve channel.

**Determination:** Model FX MTM as a separate non-operating, non-cash line (exclude from EBITDA, include in FCFE bridge). Treat the ZARONIA transition as an unquantified modelling assumption, not a verified non-event.

### 2.6 The Unresolved Reconciliation Gaps (Forensic Red Flags)

| Gap | Amount | Status |
|---|---|---|
| Swiftnet gain: P&L R4,408m vs §12.2 R1,164m | **R1,244m** | **Unexplained (Q-G26 residual, HIGH)** |
| Group tax-paid roll-forward (FY2026) | ~R32m break | Unexplained (Q-T23) |
| Company share-based reserve column | R1m FY26 / R15m FY25 | Unexplained (Q-EQ10) |
| Group cash-flow "movement in working capital" | R872m double-count | Presentation error (QQ1) |
| Service fees sub-lines vs total | R3,815m vs R5,324m | Unexplained (OO1) |
| NCI R15m vs 100%-owned BCX/Trudon | R15m | Text/table contradiction (Q-GC13) |
| Investment property cost roll-forward | R89m / R63m | Unexplained (YY1) |

---

## 3. AUDIT OF COMMON SURFACE-READING PITFALLS

| Naive reading | Forensic reality |
|---|---|
| "HEPS +21.5% — strong earnings growth" | Against a pro-forma FY2025 base of 583.2c that was itself adjusted for a R4,408m disposal gain and R618m TRF loss. Clean continuing HEPS 708.5c includes R209m factoring + R194m disposal gains management does not adjust. |
| "FCF +10.4% to R3,068m — cash generation improving" | Includes R240m new cell-captive dividend and R209m factoring gain. Clean FCF growth ~+1.8%. Cash conversion (EBITDA−capex−lease principal) only 34.3%. |
| "Net debt/EBITDA 0.5x — very low leverage" | Metric is **ex-lease** and EBITDA is **grossed up by interest income**. Including R7,556m lease liabilities, net debt is R6,426m; the ratio is flattered. |
| "No impairment on BCX/Consumer/Openserve — assets sound" | BCX discount rate cut 580bps (20.8%→15.0%) is the sole reason R1,295m goodwill survives. Consumer/Openserve breakeven sensitivities are tight (~60–70bps). |
| "Cybersecurity revenue growing robustly" (GCEO) | Actual cybersecurity revenue fell −5.5% (R469m→R443m). |
| "Mobile market-leading growth for 3 years 2 quarters" | +6.8% mobile service revenue is real, but BCX revenue fell −8.6% and blended ARPU is flat at R76. |
| "Dividend 270.10cps = 45% of FCF — within 40–60% policy" | FCF denominator includes non-recurring items; clean payout is ~50–53%. |
| "Cash tax paid R32m — tax-efficient" | −92% collapse on assessed-loss utilisation; a trough year that normalises upward, compressing future FCF. |
| "Interest-bearing debt −43% — massive deleveraging" | Genuine, but partly reflects lease reclassification (Swiftnet externalisation) and the FY2025 disposal proceeds applied in FY2026. |
| "Two fibre subscriber figures — pick the bigger one" | 597,582 vs 219,928 are irreconcilable; the 219,928 figure reconciles to 817,540 access connections × 53.1% connectivity. |

---

## 4. FINAL FORENSIC VERIFICATION MATRIX

| Junction | Raw Initial Claim | Resolving Note / SENS | Final Verified Determination |
|---|---|---|---|
| **Service revenue vs device financing** | "Revenue +1.4% to R44,477m; data-led growth" | Note 3.2 (p.36): over-time R38,336m incl. R434m interest; CPE restatement R700m | Service revenue ex-interest **R37,902m**; R434m accretion modelled separately; R3,801m non-ceded enterprise book is a declining run-off. **Verified.** |
| **ARPU & churn** | "ARPU stable; 25.7m subs; market-leading growth" | p.29 ARPU R76; p.37 vs p.29 fibre subscriber contradiction; cancellations R82m→R165m | ARPU flat, price/MB deflation ~6.7%; fibre base ~220k (not 597,582); churn signals rising. **Contradiction unresolved (N1/N4).** |
| **Tower leases & IFRS 16** | "Lease liabilities R7,556m; net debt 0.5x" | Note 6.3: remeasurement R1,417m CPI-driven; Swiftnet externalised; R359m renewals from Apr 2026 | Lease liabilities **R7,556m**, +9.2%; remeasurement structural (CPI); lease interest +19% to R630m; principal R1,910m is FCFE deduction. **Verified; guardrail applied.** |
| **Spectrum vs network capex** | "Capex R6,434m, 14.5% intensity; 184 MHz spectrum" | No spectrum cost/amortisation/rollout disclosed anywhere in AFS | **Material disclosure gap.** Spectrum capex cannot be separated; model network capex 13.5–14.5% with R8,544m uncontracted pipeline flagged discretionary. |
| **FX & hyperinflation** | "FX loss R227m; all debt local" | Note 6.2: FV adj R(372)m on USD forwards; net USD short widened to R1,586m; no IAS 29 subsidiary | FX MTM is non-operating/non-cash; hedge book mis-positioned; ZARONIA transition unquantified. **Verified; FX drag growing.** |
| **Swiftnet disposal gain** | "Gain R4,408m (P&L) / R1,164m (§12.2)" | §12.3 confirms R4,408m in discontinued-op line; §12.2 shows R1,164m | **R1,244m gap unexplained (Q-G26 HIGH).** Treat R4,408m as gross non-recurring; underlying Swiftnet EBITDA only R517m. |
| **FCF & dividend** | "FCF R3,068m; dividend 270.10cps = 45%" | Note 3.6/3.7; cell-captive dividend R240m; factoring gain R209m | Clean FCF ~R2,600–2,800m; clean payout ~50–53%. **Headline FCF overstated.** |
| **Tax** | "Effective rate 25.4%; cash tax R32m" | Note 8.1/8.2/8.3: deferred tax R944m non-cash; assessed losses utilised R325m; FY2025 19.1% flattered by disposals | Normalised effective rate **~25–26%**; cash tax trough will normalise upward; FY2025 base not comparable. **Verified.** |
| **Impairment / goodwill** | "No impairment on BCX/Consumer/Openserve" | Note 5.3: BCX discount 20.8%→15.0%; Consumer breakeven 17.6%/2.6%; Openserve 17.1%/2.2% | **No impairment is a discount-rate artefact.** Headroom is rate-sensitive; tight breakeven sensitivities. **Verified as fragile.** |
| **Debt & liquidity** | "Debt −43% to R6,593m; net cash ex-lease" | Note 6.4: all local, unsecured; covenant 3:1 (actual 0.5x); committed facilities R5,672m | Genuine deleveraging; committed liquidity ~R13.4bn vs R2,069m current maturities. **Verified strong.** |
| **SIU / contingencies** | "No material impact expected" | Note 6.8: SCA hearing 28 May 2026, judgement reserved; RSSS R529m, Phutuma R5.5bn, Masstores R166m | ~R6.2bn quantified contingent exposure, none provided; SIU outcome pending. **Unquantified tail risk.** |

---

**Audit sign-off:** The FY2026 results represent a genuine operational turnaround (cost discipline, margin expansion, deleveraging) but the *reported* quality of earnings and cash flow is materially flattered by non-recurring items, a discount-rate-driven impairment outcome, and a tax trough. The single largest unresolved forensic item is the **R1,244m Swiftnet gain reconciliation gap**, followed by the **BCX discount-rate-driven goodwill survival** and the **FCF quality overstatement**. Forecasts should be built on clean service revenue (R37,902m), normalised tax (~25–26%), lease-inclusive net debt (R6,426m), and clean FCF (~R2,600–2,800m).