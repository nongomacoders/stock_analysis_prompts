### 1. Answers to Stored Questions for This Section
No stored questions were supplied (first section capture). Nothing to answer.

### 2. Footnote & Qualification Deep-Dive
No footnote markers (`[^1]`, `*`, note references) or footnote definitions appear anywhere in the supplied D009 evidence (pp. 48–50). The tables are presented without small-print qualifications. Therefore:
- No footnote text is missing from this capture — there is simply none printed in the selected area.
- The consequential caveats in this section are instead embedded in **column structure and row labels**, which must be unpacked:
  1. **"Excluding third-party buy-in feedstock" rows** (US$ AISC and head grade, p. 48–49): the group US$ AISC is reported both including (US$1,867/oz) and excluding (US$1,798/oz) buy-in feedstock. This is an accounting/scope exclusion — the buy-in tonnes carry their own cost and grade and dilute group unit metrics. Forecast must model buy-in separately, not blend it.
  2. **"Head grade – excluding third-party buy-in feedstock"** for Evander jumps to 11.2 g/t (FY26) vs 4.8 g/t total — confirming Evander's total head grade is heavily diluted by 202,555 t of low-grade buy-in. This is a hidden grade-quality signal for Evander's own ore.
  3. **Tennant (Australia) is reported in A$ and US$ separately** with its own FX (US$/A$ 1.47 FY26 vs 1.54 FY25) — a material FX tailwind embedded in the US$ group figures that must be isolated.
  4. **FY25 vs FY26 FX**: US$/ZAR moved 18.17 → 16.90 (ZAR strengthened ~7%), which inflates US$ costs/revenue translation; must be stripped for like-for-like cost trend.
  5. **Row-label ambiguity**: "Surface operations MTR operation" column and "Tennant Mines" column are inconsistently populated across pages (e.g., p.48 tailings row shows Elikhulu 13,807,025 and a merged "11,566,768" figure; p.49 shows Tennant 32,124 oz surface feedstock). The column mapping is garbled in capture and must be verified against the printed table.

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| Q1 | High | D008.2 ALL-IN COSTS | Group US$ AISC FY26 = 1,867/oz incl. buy-in vs 1,798/oz excl. buy-in `[D009, p. 49]` | Reconcile the AISC build-up (sustaining capex, royalties, G&A, by-product) to the 1,867 and 1,798 figures; confirm which is the headline APM and the buy-in cost/oz excluded. | Determines the AISC baseline and whether buy-in is margin-accretive or dilutive. |
| Q2 | High | D008.3 SUSTAINING CAPITAL / EXPANSION CAPITAL | Capex FY26 US$214.9m vs FY25 US$163.6m (+31%); Tennant capex US$71.3m vs 35.8m `[D009, p. 50]` | Split total capex into sustaining vs expansion; confirm Tennant's step-up is expansion (MTR) vs sustaining; check FY27 guidance. | Capex is the largest AISC and FCF driver; Tennant doubling needs justification. |
| Q3 | High | D006.2 Note 3 SEGMENT ANALYSIS | Revenue ZAR17,249.1m FY26 vs 9,715.6m FY25 (+78%); cost of production ZAR6,431.7m vs 5,084.0m `[D009, p. 50]` | Reconcile segment revenue/cost to the income statement; confirm the ZAR revenue excludes the A$195.3m Tennant revenue or includes it translated. | Revenue/cost bridge underpins margin and EBITDA forecast. |
| Q4 | High | D008.4 ADJUSTED EBITDA | Adjusted EBITDA US$663.1m FY26 vs 245.8m FY25; Barberton 142.4 vs 71.0; Evander 120.9 vs 16.3 `[D009, p. 50]` | Reconcile segment Adjusted EBITDA sum (263.4+399.7 = 663.1) to group; confirm add-backs and that FX (16.90 vs 18.17) is the main swing. | EBITDA is the core forecast output; verify no one-offs inflate FY26. |
| Q5 | Medium | D008.1 FINANCIAL APMs | Average US$ gold price received Group 4,235/oz FY26 vs 2,735/oz FY25 `[D009, p. 49]` | Confirm realized price definition (spot vs hedged) and reconcile to revenue ÷ oz sold (272,373 oz). | Realized price × volume drives revenue; check hedge/lag effects. |
| Q6 | Medium | D006.2 Note 3 SEGMENT ANALYSIS | Evander gold produced 46,855 oz FY26 vs 27,829 FY25 (+68%) driven by buy-in 6,609 oz and tailings `[D009, p. 48–49]` | Confirm Evander underground vs buy-in vs tailings split and whether the uplift is sustainable or one-off buy-in. | Evander is the biggest production swing; sustainability matters for FY27 volume. |
| Q7 | Medium | D008.2 ALL-IN COSTS | Barberton US$ AISC 2,589/oz FY26 vs 2,065 FY25 (+25%) despite higher grade `[D009, p. 49]` | Reconcile Barberton AISC rise to capex (37.5 vs 24.9) and cost of production; confirm no one-off. | Barberton is highest-cost underground asset; margin risk. |
| Q8 | Medium | D006.2 Note 3 SEGMENT ANALYSIS | Tennant US$ all-in cost 4,339/oz FY26 vs 32,041 FY25 (base-effect distortion) `[D009, p. 49]` | Confirm Tennant FY25 low base (1,513 oz) and FY26 ramp (32,124 oz); check unit cost normalization. | Tennant is a new/ramping asset; FY25 base is not comparable. |
| Q9 | Low | D010 Glossary | Column mapping garbled: "Surface operations MTR operation" vs "Tennant Mines" inconsistent `[D009, p. 48–50]` | Confirm definition of MTR operation vs Tennant Mines and which columns aggregate to Group. | Ensures segment totals are correctly attributed in the model. |

### 4. Updated Open Questions Ledger
```json
{"ledger_version": 1, "updates": [], "new_questions": [
{"question": "Reconcile group US$ AISC FY26 of 1,867/oz (incl. third-party buy-in feedstock) vs 1,798/oz (excl. buy-in) to the AISC build-up; confirm which is the headline APM and the buy-in cost/oz excluded.", "priority": "high", "target_document": "Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf", "target_section": "D008.2 ALL-IN COSTS", "evidence_required": "AISC reconciliation table (sustaining capex, royalties, G&A, by-product credits, buy-in adjustment) for FY26 and FY25, in US$/oz, with the 1,867 and 1,798 figures tied out.", "closure_condition": "Both AISC figures reconciled to components; headline APM identified; buy-in exclusion quantified; forecast consequence stated."},
{"question": "Split FY26 total capex of US$214.9m (vs US$163.6m FY25) into sustaining vs expansion, and confirm whether Tennant's US$71.3m (vs 35.8m) is expansion (MTR) or sustaining; obtain FY27 capex guidance.", "priority": "high", "target_document": "Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf", "target_section": "D008.3 SUSTAINING CAPITAL, EXPANSION CAPITAL, NET (CASH)/DEBT", "evidence_required": "Sustaining vs expansion capex table by operation for FY26/FY25 in US$m, plus any FY27 guidance; Tennant MTR project capex disclosure.", "closure_condition": "Capex split confirmed and FY27 guidance captured; forecast capex line set."},
{"question": "Reconcile segment revenue ZAR17,249.1m and cost of production ZAR6,431.7m (FY26) to the consolidated income statement, and confirm whether A$195.3m Tennant revenue is included translated or excluded.", "priority": "high", "target_document": "Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf", "target_section": "D006.2 Note 3 SEGMENT ANALYSIS", "evidence_required": "Segment-to-group revenue and cost reconciliation in ZAR, with FX translation of Tennant A$ revenue at 16.90/1.47; tie to income statement totals.", "closure_condition": "Segment totals reconcile to group income statement; Tennant translation treatment confirmed."},
{"question": "Reconcile segment Adjusted EBITDA (Barberton 142.4 + Evander 120.9 + surface 399.7 = 663.1 US$m) to group and confirm add-backs/one-offs and the FX swing (16.90 vs 18.17) contribution.", "priority": "high", "target_document": "Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf", "target_section": "D008.4 ADJUSTED EBITDA", "evidence_required": "Adjusted EBITDA reconciliation from operating profit, listing add-backs, and FX impact quantification FY26 vs FY25.", "closure_condition": "EBITDA reconciliation complete; one-offs and FX isolated; clean FY26 EBITDA baseline established."},
{"question": "Confirm realized gold price definition (spot vs hedged) and reconcile group average US$4,235/oz FY26 to revenue divided by 272,373 oz sold.", "priority": "medium", "target_document": "Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf", "target_section": "D008.1 FINANCIAL APMs", "evidence_required": "Realized price methodology note and revenue/oz reconciliation; hedge or pricing-lag disclosure.", "closure_condition": "Realized price definition confirmed and reconciled to revenue; hedge/lag effects quantified."},
{"question": "Confirm Evander FY26 production uplift to 46,855 oz (vs 27,829) split between underground, buy-in (6,609 oz) and tailings, and whether the buy-in component is sustainable into FY27.", "priority": "medium", "target_document": "Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf", "target_section": "D006.2 Note 3 SEGMENT ANALYSIS", "evidence_required": "Evander production split by source FY26/FY25 and any commentary on buy-in feedstock sustainability/contracts.", "closure_condition": "Evander source split confirmed; sustainable vs one-off volume identified for FY27 forecast."},
{"question": "Reconcile Barberton US$ AISC rise to 2,589/oz (vs 2,065) against capex (37.5 vs 24.9) and cost of production; confirm no one-off.", "priority": "medium", "target_document": "Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf", "target_section": "D008.2 ALL-IN COSTS", "evidence_required": "Barberton AISC build-up FY26/FY25 with capex and cost components; note any one-off items.", "closure_condition": "Barberton AISC rise fully explained; recurring vs one-off isolated."},
{"question": "Confirm Tennant FY25 low base (1,513 oz) and FY26 ramp (32,124 oz) and normalize unit costs (US$ all-in cost 4,339/oz FY26 vs 32,041 FY25) for a comparable run-rate.", "priority": "medium", "target_document": "Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf", "target_section": "D006.2 Note 3 SEGMENT ANALYSIS", "evidence_required": "Tennant production and cost history FY25/FY26 with ramp commentary and normalized unit cost.", "closure_condition": "Tennant ramp understood; normalized cost/oz established for forecast."},
{"question": "Confirm definition of 'Surface operations MTR operation' vs 'Tennant Mines' columns and which columns aggregate to Group totals, given inconsistent column mapping in the production summary.", "priority": "low", "target_document": "Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf", "target_section": "D010 Glossary", "evidence_required": "Glossary/definition of MTR operation and Tennant Mines; confirmation of segment aggregation to Group.", "closure_condition": "Column definitions confirmed; segment attribution verified against printed table."}
]}
```

### 5. Baseline Forecast Inputs Captured Here

| Metric | FY26 | FY25 | Unit |
| --- | --- | --- | --- |
| Tonnes milled – underground (Group) | 395,154 | 388,884 | t |
| Tonnes milled – surface (Barberton) | 62,276 | 65,288 | t |
| Tonnes processed – tailings (Group) | 26,149,178 | 22,924,167 | t |
| Tonnes processed – surface feedstock (Tennant) | 751,914 | 85,316 | t |
| Tonnes processed – third-party buy-in (Group) | 887,646 | 92,536 | t |
| Head grade – total (Group) | 0.5 | 0.5 | g/t |
| Overall recovery – underground (Group) | 94 | 91 | % |
| Overall recovery – tailings (Group) | 47 | 40 | % |
| Gold produced – underground (Group) | 105,478 | 93,724 | oz |
| Gold produced – tailings (Group) | 113,613 | 98,636 | oz |
| Gold produced – buy-in (Group) | 18,667 | 1,081 | oz |
| Gold produced – surface feedstock (Tennant) | 32,124 | 1,513 | oz |
| **Gold produced – total (Group)** | **272,310** | **196,527** | oz |
| Gold sold – total (Group) | 272,373 | 196,926 | oz |
| Avg US$ gold price received (Group) | 4,235 | 2,735 | US$/oz |
| Avg ZAR gold price received (Group) | 2,308,329 | 1,595,761 | ZAR/kg |
| Avg A$ gold price received (Tennant) | 195,501 | 162,171 | A$/kg |
| US$ cash cost (Group) | 1,600 | 1,426 | US$/oz |
| US$ AISC (Group) | 1,867 | 1,600 | US$/oz |
| US$ AISC excl. buy-in (Group) | 1,798 | 1,599 | US$/oz |
| US$ all-in cost (Group) | 2,576 | 2,383 | US$/oz |
| ZAR cash cost (Group) | 860,706 | 835,034 | ZAR/kg |
| ZAR AISC (Group) | 985,551 | 934,517 | ZAR/kg |
| ZAR all-in cost (Group) | 1,271,855 | 1,287,842 | ZAR/kg |
| A$ cash cost (Tennant) | 81,099 | 43,116 | A$/kg |
| A$ AISC (Tennant) | 106,900 | 80,962 | A$/kg |
| A$ all-in cost (Tennant) | 205,143 | 1,584,835 | A$/kg |
| Capital expenditure (Group) | 214.9 | 163.6 | US$m |
| Revenue (Group, ZAR) | 17,249.1 | 9,715.6 | ZAR m |
| Revenue (Tennant, A$) | 195.3 | 5.9 | A$ m |
| Cost of production (Group, ZAR) | 6,431.7 | 5,084.0 | ZAR m |
| Cost of production (Tennant, A$) | 81.0 | 1.6 | A$ m |
| All-in sustaining cost of production (Group, ZAR) | 6,595.8 | 5,689.7 | ZAR m |
| All-in cost of production (Group, ZAR) | 8,735.2 | 7,841.0 | ZAR m |
| Adjusted EBITDA (Group) | 663.1 | 245.8 | US$m |
| Avg FX US$/ZAR | 16.90 | 18.17 | — |
| Avg FX US$/A$ | 1.47 | 1.54 | — |

### 6. Next Section to Capture
**D008.2 ALL-IN COSTS** (physical pp. 40–43) — resolves Q1 and Q7 (AISC build-up and Barberton AISC rise), and supports Q5 (realized price). If AISC detail is thin, **D008.3** (p. 44) resolves Q2 (sustaining vs expansion capex).