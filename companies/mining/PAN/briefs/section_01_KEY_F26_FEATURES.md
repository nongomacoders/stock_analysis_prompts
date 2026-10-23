# Section 01: KEY F26 FEATURES

> **Package**: `section-79b053c261e7412ea9a8d9918d715d1f`  
> **Report**: `Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf` (annual_report)  
> **Model**: `deepseek/deepseek-v4.1-flash-1017`  
> **Execution Time**: 35.12s  
> **Cost**: $0.0022  
> **Tokens**: 11,486 total (7,353 prompt / 4,133 completion)  

### 1. Answers to Stored Questions for This Section
*(No stored questions were supplied — this is the first captured section. Proceeding to footnote/qualification unpacking and new question generation.)*

### 2. Footnote & Qualification Deep-Dive

No explicit footnote markers (`[^1]`, `*`) with definitions appear in the supplied D002 evidence. However, several **embedded qualifications and small-print caveats** function as de-facto footnotes and materially change interpretation of the headline numbers:

- **"Lower-cost operations, which account for 90.8% of annual production, achieved an AISC of US$1,702/oz"** `[D002, physical PDF p. 2–3]` — This is a subset metric, not a group metric. The qualification "exclude only Barberton Mines' Sheba and Consort Mines" `[D002, p. 3]` means the residual ~9.2% of production (Sheba + Consort) carries an implied AISC far above the group US$1,867/oz. **Arithmetic tension to flag:** if 90.8% of ounces cost US$1,702/oz and the group blended is US$1,867/oz, the excluded 9.2% must carry an implied AISC of roughly US$3,500/oz (solve: 0.908×1,702 + 0.092×X = 1,867 → X ≈ 3,495). This is a critical forecast input — the high-cost tail is a drag that must be modelled separately, and the "90.8%" denominator (which production base?) needs verification.

- **"within cost guidance for FY26 of between US$1,820/oz and US$1,870/oz"** `[D002, p. 3]` — US$1,867/oz sits at the very top of the guided range. The "within guidance" framing masks that the group landed at the ceiling, consistent with the listed adverse drivers (stronger ZAR, third-party material processing, Tennant ramp-up shortfall, share-based payments, royalties). Forecast implication: no cost cushion carried into FY27.

- **"strengthened US$/ZAR exchange rate of US$/ZAR:16.90 compared to guidance of US$/ZAR:18.50, which adversely impacted unit costs"** `[D002, p. 3]` — A ~8.7% stronger ZAR than guided. This is the single largest identifiable cost headwind and must be isolated when building the FY27 cost bridge (FY27 guidance assumes US$/ZAR:17.00, i.e., a ~0.6% weaker ZAR than FY26 actual — a modest tailwind vs. FY26 actual but still far stronger than the FY26 guidance rate).

- **"Tennant Mines produced 32,124oz in FY26, following slower-than-anticipated ramp-up... expected to increase FY27 production to between 48,000oz and 52,000oz"** `[D002, p. 3]` — A step-change of +16,000–20,000oz guided for FY27, contingent on fixed crusher circuit, secondary mill, belt filter, and higher-grade White Devil feed. This is a forward-looking claim resting on capex not yet evidenced as commissioned — must be verified against capex and production sections.

- **"Soweto Cluster DFS... NPV13 of ~US$109 million and a payback period of less than three years at current gold prices... (at US$/ZAR:17.00)"** `[D002, p. 3]` — The NPV/payback is explicitly struck at a US$/ZAR:17.00 deck and "current gold prices." The gold price assumption is NOT stated in this capture — a missing-input flag. FID expected December 2026, so US$216m capex is a post-FY27 commitment, not an FY27 cash item, but must be tracked for financing.

- **"White Devil... approximately 3Mt at 3.8g/t (~350Koz)... supporting production of approximately 50,000oz per annum... towards approximately 100,000oz per annum over the next five years"** `[D002, p. 3]` — Multi-year ramp claim; the ~350Koz reserve at 50Koz/yr implies ~7-year life at that rate, yet the 100Koz target "over five years" needs reconciliation against reserve ounces. Flag for reserve/LoM verification.

- **"Royal Sheba... around 40,000oz per year at steady state... first blast scheduled for early 2027"** `[D002, p. 3]` — First blast early 2027 = FY27 (Jul 2026–Jun 2027) at earliest; steady-state 40Koz is a multi-year-out item, NOT an FY27 contributor. Must not be double-counted with BTRP existing production.

- **"water cost savings of US$1.4 million per year"** and **"Savings of US$5.1 million... from renewable energy"** `[D002, p. 2–3]` — These are stated as run-rate savings; the US$5.1m is FY26 realised, the US$1.4m is forward ("expects"). Treat US$1.4m as an FY27+ cost tailwind, not yet in the FY26 base.

- **Dividend arithmetic check** `[D002, p. 2]`: Final ZAR 1,583.6m ÷ ZA 65.00000c/share = 2,436.3m shares implied. Interim ZAR 280.0m ÷ ZA 12.00000c = 2,333.3m shares implied. **Discrepancy:** implied share count rose ~103m shares between interim and final — consistent with the Emmerson acquisition (completed 22 June 2026) issuing shares, but the exact share count and Emmerson consideration structure must be verified. Total ZAR 1,863.6m ÷ ZA 77.0c = 2,420.3m shares — a third implied count. These three implied counts do not reconcile cleanly and must be checked against the actual weighted/issued share count in the financial statements.

- **US$ conversion check** `[D002, p. 2]`: ZAR 1,863.6m ≈ US$113.6m implies ~US$/ZAR 16.40; ZAR 1,583.6m ≈ US$96.2m implies ~16.46. These differ from the stated average rate of 16.90 — likely a spot/declared-rate conversion at dividend declaration date, not the average. Flag the FX rate used for dividend conversion.

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| Q1 | High | D009 Group production summary | Lower-cost ops = 90.8% of production at US$1,702/oz; group US$1,867/oz; excludes Sheba & Consort `[D002, p. 2–3]` | Confirm total group ounces, ounces from Sheba+Consort, and their individual AISC; reconcile to the implied ~US$3,500/oz tail | High-cost tail is a material drag; must model separately, not blend |
| Q2 | High | D008 Alternative performance measures | AISC definition and reconciliation to "within guidance US$1,820–1,870/oz" `[D002, p. 3]` | Obtain AISC reconciliation table (by operation and group), confirm what is included/excluded (royalties, share-based payments, third-party processing) | AISC is the core unit-cost forecast driver; definitional scope changes the number |
| Q3 | High | D006 Financial notes | Dividend implied share counts: 2,436m (final), 2,333m (interim), 2,420m (total) `[D002, p. 2]` | Check issued/weighted share count, Emmerson share consideration, and treasury shares; reconcile the three implied counts | Share count drives EPS, DPS, and per-share forecasts |
| Q4 | High | D006 Financial notes | Dividend FX: ZAR→US$ conversions imply ~16.40–16.46 vs stated avg 16.90 `[D002, p. 2]` | Confirm FX rate and date used for dividend US$ conversion | Affects US$ dividend and cash flow forecast |
| Q5 | High | D003 CEO's statement / D009 | Tennant FY27 guidance 48,000–52,000oz vs FY26 32,124oz `[D002, p. 3]` | Verify capex committed/commissioned for fixed crusher, secondary mill, belt filter; confirm White Devil first blast Aug 2026 and grade ramp | Largest single production step-change in FY27; hinges on plant capex delivery |
| Q6 | Medium | D009 Group production summary | Elikhulu 56,475oz @ US$1,231/oz; MTR 51,927oz @ US$1,389/oz `[D002, p. 3]` | Confirm these are full-year and reconcile to group total; check MTR expansion (Dec 2025) run-rate into FY27 | Surface ops are the low-cost engine; run-rate vs. full-year matters for FY27 |
| Q7 | Medium | D003 CEO's statement | Evander underground grade >11g/t FY26 vs 6.8g/t FY25; production +68.4% `[D002, p. 3]` | Verify grade sustainability into FY27 (24 Level B raise line) and whether 11g/t is repeatable or a one-off high-grade campaign | Grade is the key Evander cost/revenue driver; sustainability critical |
| Q8 | Medium | D006 Financial notes / D008 | Soweto Cluster DFS: US$216m capex, NPV13 ~US$109m, payback <3yr "at current gold prices" `[D002, p. 3]` | Confirm gold price assumption in DFS; confirm FID timing (Dec 2026) and financing plan; confirm capex is post-FY27 | US$216m is a future funding commitment; gold price deck missing |
| Q9 | Medium | D009 / D006 | White Devil ~3Mt @ 3.8g/t (~350Koz) supporting ~50Koz/yr then ~100Koz/yr over 5 years `[D002, p. 3]` | Reconcile reserve ounces to the 50→100Koz ramp; check LoM implied | Multi-year production trajectory; reserve-to-plan consistency |
| Q10 | Medium | D003 CEO's statement | Royal Sheba ~40Koz/yr steady state, first blast early 2027 `[D002, p. 3]` | Confirm first production timing and whether any FY27 ounces; confirm not double-counted with BTRP | Avoid overstating FY27 production |
| Q11 | Low | D008 / D006 | Renewable energy savings US$5.1m realised FY26; water savings US$1.4m/yr expected `[D002, p. 2–3]` | Confirm US$5.1m is in FY26 base (not additive to FY27) and US$1.4m is incremental FY27+ | Prevents double-counting cost savings in FY27 bridge |
| Q12 | Low | D006 Financial notes | Share-based payment expense elevated due to share price `[D002, p. 3]` | Quantify SBP expense FY26 vs FY25 and FY27 assumption | Non-cash but in AISC; affects cost forecast |
| Q13 | Low | D005 Primary financial statements | Emmerson acquisition completed 22 June 2026 `[D002, p. 3]` | Confirm consolidation date, purchase consideration, goodwill/PPA, and any FY27 contribution | Affects FY27 balance sheet, share count, and possibly production |

### 4. Updated Open Questions Ledger (Copy to App)

```markdown
# OPEN QUESTIONS LEDGER — after D002 (Highlights)

## Pending: D003 (CEO's statement)
- Q5: Verify Tennant FY27 guidance 48,000–52,000oz vs FY26 32,124oz; confirm capex for fixed crusher, secondary mill, belt filter; White Devil first blast Aug 2026 and grade ramp. [D002, p.3]
- Q7: Verify Evander underground grade >11g/t FY26 (vs 6.8g/t FY25) sustainability into FY27; is it repeatable or one-off? [D002, p.3]
- Q10: Confirm Royal Sheba first production timing (first blast early 2027) and whether any FY27 ounces; confirm not double-counted with BTRP. [D002, p.3]

## Pending: D005 (Primary financial statements)
- Q13: Confirm Emmerson acquisition consolidation date (22 June 2026), purchase consideration, goodwill/PPA, FY27 contribution. [D002, p.3]

## Pending: D006 (Financial notes)
- Q3: Reconcile dividend implied share counts: 2,436m (final), 2,333m (interim), 2,420m (total); check issued/weighted count, Emmerson shares, treasury. [D002, p.2]
- Q4: Confirm FX rate/date used for dividend US$ conversion (implied ~16.40–16.46 vs stated avg 16.90). [D002, p.2]
- Q8: Confirm Soweto Cluster DFS gold price assumption; FID timing Dec 2026; financing plan; capex post-FY27. [D002, p.3]
- Q12: Quantify share-based payment expense FY26 vs FY25 and FY27 assumption. [D002, p.3]

## Pending: D008 (Alternative performance measures)
- Q2: Obtain AISC reconciliation (by operation and group); confirm inclusions/exclusions (royalties, SBP, third-party processing) vs guidance US$1,820–1,870/oz. [D002, p.3]
- Q11: Confirm renewable energy US$5.1m is in FY26 base (not additive to FY27); water savings US$1.4m/yr is incremental FY27+. [D002, p.2–3]

## Pending: D009 (Group production summary)
- Q1: Confirm total group ounces, Sheba+Consort ounces and their AISC; reconcile to implied ~US$3,500/oz tail (90.8% at US$1,702/oz vs group US$1,867/oz). [D002, p.2–3]
- Q6: Confirm Elikhulu 56,475oz @ US$1,231/oz and MTR 51,927oz @ US$1,389/oz are full-year; check MTR expansion (Dec 2025) run-rate into FY27. [D002, p.3]
- Q9: Reconcile White Devil ~3Mt @ 3.8g/t (~350Koz) to 50→100Koz/yr ramp over 5 years; check implied LoM. [D002, p.3]
```

### 5. Baseline Forecast Inputs Captured Here

| Metric | FY26 | FY25 | Note |
| --- | --- | --- | --- |
| Group AISC | US$1,867/oz | US$1,600/oz | Top of guidance US$1,820–1,870/oz |
| Lower-cost ops AISC | US$1,702/oz | US$1,434/oz | 90.8% of production (FY25: 86.2%) |
| Avg US$/ZAR | 16.90 | 18.17 | Guidance was 18.50 |
| FY27 AISC guidance | US$2,075–2,175/oz | — | Assumes US$/ZAR:17.00 |
| Elikhulu production | 56,475oz | 52,606oz | AISC US$1,231/oz (FY25: 1,077) |
| MTR production | 51,927oz | 30,806oz | AISC US$1,389/oz (FY25: 1,282); expansion commissioned Dec 2025 |
| Tennant production | 32,124oz | — | FY27 guidance 48,000–52,000oz |
| Barberton UG production | 71,997oz | 68,549oz | +5.6% |
| Evander production | 46,854oz | 27,829oz | +68.4%; UG grade >11g/t (FY25: 6.8g/t) |
| Final dividend | ZAR 1,583.6m (~US$96.2m) | — | ZA 65.0c/share (~US3.94897c; 2.98576p) |
| Interim dividend | ZAR 280.0m | — | ZA 12.0c/share |
| Total dividend | ZAR 1,863.6m (~US$113.6m) | — | ZA 77.0c/share |
| Renewable energy savings | US$5.1m | US$4.2m | Realised |
| Water savings (expected) | US$1.4m/yr | — | Forward run-rate |
| Soweto Cluster DFS | US$216m capex; NPV13 ~US$109m; payback <3yr | — | FID Dec 2026; at US$/ZAR:17.00 |
| White Devil reserve | ~3Mt @ 3.8g/t (~350Koz) | — | First blast Aug 2026 |
| Royal Sheba | ~40Koz/yr steady state | — | First blast early 2027; LoM ≥11yr |
| LTIFR / RIFR / TRIFR | 1.41 / 0.55 / 5.51 | 1.58 / 0.85 / 6.56 | Per million man hours |
| Fatalities | 1 | 2 | Underground |

### 6. Next Section to Capture
**`D003` (CEO's statement, pp. 5–15)** — will resolve Q5 (Tennant FY27 ramp/capex), Q7 (Evander grade sustainability), and Q10 (Royal Sheba timing), and likely provide the gold price deck and FY27 production/cost outlook narrative needed to anchor the forecast.