# Section 04: Financial notes — Notes 1, 2

> **Package**: `section-4568f3579bff4ffaab6a5b6e08d98108`  
> **Report**: `Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf` (annual_report)  
> **Model**: `deepseek/deepseek-v4.1-flash-1017`  
> **Execution Time**: 34.25s  
> **Cost**: $0.0021  
> **Tokens**: 10,842 total (6,849 prompt / 3,993 completion)  

### 1. Answers to Stored Questions for This Section

**Q26: Confirm deferred tax liability +110m drivers and FY27 effective tax rate. [D005.1, p.17]**
- **Status**: `Partially resolved (remainder stays open for D006 Financial notes)`
- **Answer & evidence**: This section confirms the *methodology* but not the *quantum*. It states South African gold mining income tax is determined by the "gold formula" taking into account taxable income and revenue from gold mining operations, and that judgement was applied in determining future expected deferred tax rates of the Group's mining operations. Deferred tax is calculated at rates expected to apply when the asset is realised/liability settled, based on enacted/substantively enacted rates, with rates based on management's best estimate of when temporary differences will be utilised over the life of the mining operations `[D006.1, physical PDF p. 19–20]`. This explains *why* the DTL can move materially (formula-based rates + judgement on realisation timing) but does **not** quantify the +110m driver or give an FY27 effective tax rate. Remainder stays open for the deferred tax note (D006).

**Q27: Confirm note 14/15 cross-references (footnote numbering gap [^2] undefined). [D005.1, p.19]**
- **Status**: `Partially resolved`
- **Answer & evidence**: This capture shows Notes 1 (Basis of preparation) and 2 (Judgements and estimates) with no footnote markers (`[^1]`, `[^2]`, `*`) present in the supplied text `[D006.1, physical PDF p. 19–20]`. The footnote-numbering gap flagged at D005.1 is therefore not resolved here; the note numbering in this section runs 1, 2 sequentially with no visible footnote definitions. Remainder (locating the missing [^2] definition) stays open for later D006 pages.

**Q28: Confirm nature/liquidity of short-term investments 137,867 and investments 12,791; restricted cash 2,612. [D005.1, p.17–18]**
- **Status**: `Partially resolved (remainder stays open for D006 Financial notes)`
- **Answer & evidence**: This section aggregates "cash and cash equivalents and short-term investments" at **US$246.2m** (FY25: US$49.5m) as at 30 June 2026 `[D006.1, physical PDF p. 19]`. This is consistent with combining the balance-sheet cash plus short-term investments flagged earlier, but the split between cash, short-term investments (137,867) and the 12,791 investments / 2,612 restricted cash is **not** broken out here. Remainder stays open for the cash/investments note.

**Q29: Confirm drivers of contract liability 8,030 and other receivables 41,654. [D005.1, p.17]**
- **Status**: `Not addressed in this section` — carried forward unchanged.

**Q13 (remainder), Q22, Q23, Q24, Q25, Q3, Q4, Q8, Q12, Q16, Q19**: Not addressed by this section's evidence (basis of preparation / judgements only). Carried forward unchanged.

---

### 2. Footnote & Qualification Deep-Dive

No footnote markers (`[^1]`, `[^2]`, `*`) or footnote definitions appear in the supplied D006.1 text `[D006.1, physical PDF p. 19–20]`. The material qualifications are instead embedded in the going-concern and judgements narrative:

- **Going concern — gold price deck (critical forecast input)** `[D006.1, physical PDF p. 19]`: Base case assumes **initial gold price US$4,600/oz rising to US$4,900/oz** for the next reporting period; downside case **US$3,680/oz with a 10% production reduction**. Forecast horizon extends to **30 June 2028**. This is a semi-static deck, not spot. *Implication*: management's own liquidity test is run well above the ~US$1,867/oz group AISC and above the DFS/study price assumptions flagged in Q8 — so the going-concern conclusion is not a stress test at current spot if spot is below US$4,600. Must verify the actual FY26 realised gold price and the FY27 budget price deck in D008/D009 to see whether the forecast model should use US$4,600 or a lower/market deck.
- **Liquidity headroom** `[D006.1, physical PDF p. 19]`: Available debt facilities **US$78.9m** (FY25: US$50.2m) and cash + short-term investments **US$246.2m** (FY25: US$49.5m). The large YoY jump in liquidity (cash+STI up ~US$197m) needs reconciling to the cash flow statement and to the Emmerson acquisition/equity raise — verify in D005/D006 cash note.
- **Deferred tax judgement** `[D006.1, physical PDF p. 19–20]`: Gold-formula tax + judgement on realisation timing = DTL is estimate-sensitive. This is the mechanism behind the +110m DTL move (Q26); the quantum must come from the deferred tax note.
- **Impairment / valuation sensitivity** `[D006.1, physical PDF p. 20]`: Cash flow projections for CGU impairment testing are "significantly affected" by Mineral Resources/Reserves, commodity prices, FX, discount rates, production costs and future capex. *Implication*: any FY26 impairment or reversal is a non-cash one-off that must be excluded from underlying forecast; verify whether any impairment was booked and its drivers in the PPE/impairment note.

---

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| Q30 | High | D006 (Financial notes) | Going-concern base case gold deck US$4,600→US$4,900/oz; downside US$3,680/oz + 10% production cut `[D006.1, p. 19]` | Locate the price/FX assumptions note and the FY27 budget price deck; confirm whether the forecast model should use US$4,600 or a market/spot deck; check FX rate assumed | Sets the revenue deck for FY27–FY28 forecast; a US$4,600 deck vs spot materially changes revenue and AISC margin |
| Q31 | High | D006 (Financial notes) | Cash + STI US$246.2m vs FY25 US$49.5m (+~US$197m); debt facilities US$78.9m `[D006.1, p. 19]` | Reconcile to cash flow statement and to Emmerson acquisition/equity issuance; confirm split of cash vs short-term investments (137,867) vs investments (12,791) vs restricted cash (2,612) | Determines net debt, liquidity and funding capacity for FY27 capex/dividends |
| Q32 | High | D006 (Financial notes) | Deferred tax: gold-formula rates + judgement on realisation timing `[D006.1, p. 19–20]` | Extract deferred tax note: quantify the +110m DTL movement drivers and the FY27 expected effective tax rate | Drives FY27 tax charge and NPAT forecast |
| Q33 | Medium | D006 (Financial notes) | Impairment testing sensitive to prices, FX, discount rates, costs, capex `[D006.1, p. 20]` | Check PPE/impairment note for any FY26 impairment/reversal, CGU carrying values, and discount rate/price assumptions used | Non-cash one-offs must be excluded from underlying forecast; signals asset carrying-value risk |
| Q34 | Medium | D006 (Financial notes) | APMs "further information on page 72" `[D006.1, p. 19]` | Confirm page 72 APM reconciliation is captured in D008 and that AISC/APM definitions match the going-concern and segment figures | Ensures APM-based forecast (AISC, all-in cost) ties to IFRS statements |
| Q35 | Low | D006 (Financial notes) | Note numbering runs 1, 2 with no footnote markers; earlier [^2] gap `[D006.1, p. 19–20]` | Confirm whether any footnote definitions for Notes 1–2 exist on adjacent pages; resolve the D005.1 [^2] numbering gap | Data-integrity check on note cross-references |

---

### 4. Updated Open Questions Ledger (Copy to App)

```markdown
# OPEN QUESTIONS LEDGER — after D006.1 (Notes 1,2 — Basis of preparation / Judgements)

## Pending: D006 (Financial notes)
- Q26 (remainder): Quantify deferred tax liability +110m drivers; extract FY27 expected effective tax rate from deferred tax note. [D005.1, p.17; D006.1, p.19–20]
- Q27 (remainder): Resolve note 14/15 cross-reference and undefined [^2] footnote numbering gap. [D005.1, p.19; D006.1, p.19–20]
- Q28 (remainder): Confirm split of cash vs short-term investments 137,867 vs investments 12,791 vs restricted cash 2,612; reconcile to US$246.2m cash+STI. [D005.1, p.17–18; D006.1, p.19]
- Q29: Confirm drivers of contract liability 8,030 and other receivables 41,654. [D005.1, p.17]
- Q30: Confirm FY27 budget gold price deck (going-concern base US$4,600→US$4,900/oz; downside US$3,680/oz +10% production cut) and FX assumption; decide forecast deck. [D006.1, p.19]
- Q31: Reconcile cash+STI US$246.2m (FY25 US$49.5m) and debt facilities US$78.9m to cash flow statement and Emmerson/equity issuance. [D006.1, p.19]
- Q32: Extract deferred tax note — quantify +110m DTL drivers and FY27 effective tax rate. [D006.1, p.19–20]
- Q33: Check PPE/impairment note for FY26 impairment/reversal, CGU carrying values, discount rate/price assumptions. [D006.1, p.20]
- Q34: Confirm page 72 APM reconciliation captured in D008; AISC/APM definitions tie to IFRS. [D006.1, p.19]
- Q35: Confirm whether footnote definitions for Notes 1–2 exist on adjacent pages; resolve [^2] gap. [D006.1, p.19–20]
- Q13 (remainder): Confirm Emmerson consolidation date (22 Jun 2026), consideration split (shares vs cash), goodwill/PPA/bargain treatment, FY27 contribution. [D002, p.3; D005.1, p.17,19]
- Q22: Confirm what "Shares to be issued" US$148,218k relates to (Emmerson?), number of shares, issue price, timing. [D005.1, p.17,19]
- Q23: Confirm Emmerson consideration split, fair value of net assets, goodwill vs bargain gain, consolidation date. [D005.1, p.17]
- Q24: Confirm reciprocal dividend (8,847) is cash round-trip on 13.1% treasury; net vs gross; FY27 dividend policy. [D005.1, p.18–19]
- Q25: Extract FY26 SBP P&L charge and FY27 expected charge; explain "Other expenses" 85,958 vs 36,484. [D005.1, p.17–18]

## Pending: D008 (Alternative performance measures)
- Q2: Obtain AISC reconciliation (by operation and group); confirm inclusions/exclusions vs guidance US$1,820–1,870/oz. [D002, p.3]
- Q11: Confirm renewable energy US$5.1m is in FY26 base (not additive to FY27); water savings US$1.4m/yr is incremental FY27+. [D002, p.2–3]
- Q20: Reconcile Elikhulu US$1,231/oz, MTR US$1,389/oz, BTRP US$1,564/oz to group AISC; confirm BTRP cost spike drivers. [D003, p.6]

## Pending: D009 (Group production summary)
- Q1: Confirm total group ounces, Sheba+Consort ounces and their AISC; reconcile to implied ~US$3,500/oz tail. [D002, p.2–3]
- Q6: Confirm Elikhulu 56,475oz @ US$1,231/oz and MTR 51,927oz @ US$1,389/oz are full-year; check MTR expansion run-rate into FY27. [D002, p.3]
- Q9: Reconcile White Devil ~3Mt @ 3.8g/t (~350Koz) to 50→100Koz/yr ramp over 5 years; check implied LoM. [D002, p.3]
- Q5 (remainder): Confirm Tennant FY27 capex $ amounts; White Devil first blast date and grade ramp. [D002, p.3; D003, p.6]
- Q7 (remainder): Confirm Evander underground grade >11g/t FY26 sustainability into FY27. [D002, p.3]
- Q10 (remainder): Confirm Royal Sheba first production timing and whether any FY27 ounces; not double-counted with BTRP. [D002, p.3; D003, p.6]
- Q14: Check FY27 MTR production split; H1 FY27 below nameplate, Q2–Q4 step-up to ~60Koz annualised. [D003, p.6]
- Q15: Check FY27 BTRP guidance; flotation benefit in FY27 or FY28. [D003, p.6]
- Q17: Check Elikhulu FY27 guidance vs FY26 56,475oz; Winkelhaak feed contribution. [D003, p.6]
- Q18: Check FY27 Tennant grade assumption and White Devil strip ratio/grade. [D003, p.6]
- Q21: Confirm Fairview 47,678oz vs table 47,677oz rounding; which used in group total. [D003, p.6–7]

## Pending: D002 / D003 (Highlights / CEO statement)
- Q3: Reconcile dividend implied share counts: 2,436m (final), 2,333m (interim), 2,420m (total); check issued/weighted count, Emmerson shares, treasury. [D002, p.2]
- Q4: Confirm FX rate/date used for dividend US$ conversion (implied ~16.40–16.46 vs stated avg 16.90). [D002, p.2]
- Q8: Confirm Soweto Cluster DFS gold price assumption; FID timing Dec 2026; financing plan; capex post-FY27. [D002, p.3]
- Q12: Quantify share-based payment expense FY26 vs FY25 and FY27 assumption. [D002, p.3]
- Q16: Locate Tennant FY27 capex $ for fixed crusher, secondary mill, belt filter; capitalised vs expensed. [D003, p.6]
- Q19: Extract total FY27 group capex guidance and Tennant-specific split. [D003, p.6]
```

---

### 5. Baseline Forecast Inputs Captured Here

| Item | Value | Source |
| --- | --- | --- |
| Available debt facilities (30 Jun 2026) | US$78.9m (FY25: US$50.2m) | [D006.1, p.19] |
| Cash + cash equivalents + short-term investments (30 Jun 2026) | US$246.2m (FY25: US$49.5m) | [D006.1, p.19] |
| Going-concern horizon | Through 30 June 2028 | [D006.1, p.19] |
| Base-case gold price deck | US$4,600/oz initial → US$4,900/oz next reporting period | [D006.1, p.19] |
| Downside-case gold price | US$3,680/oz + 10% production reduction | [D006.1, p.19] |
| Tax basis (SA gold) | Gold-formula tax on taxable income & gold revenue; judgement on deferred tax rates | [D006.1, p.19–20] |
| APM reference | Further info "page 72" | [D006.1, p.19] |

---

### 6. Next Section to Capture

**D006 (Financial notes), physical PDF pp. 21–36** — specifically the notes covering **deferred tax (Q26/Q32), cash & short-term investments (Q28/Q31), Emmerson acquisition/consideration (Q13/Q22/Q23), share-based payments & other expenses (Q25), and PPE/impairment (Q33)**. This is the single most useful next capture to resolve the highest-priority open items (Q26, Q28, Q30, Q31, Q32, Q33) and to build the FY27 tax, net-debt and capex baseline.