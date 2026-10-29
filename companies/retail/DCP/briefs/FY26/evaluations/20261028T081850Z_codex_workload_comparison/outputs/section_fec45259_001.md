### 1. Stored Questions Answered in This Section

No stored questions from earlier sections were supplied in this capture (the stored-question block is empty). The section-specific questions listed in the prompt target other documents (the AFS and the Analyst Presentation) and cannot be tested against this D001 cover/contents/about-this-report capture; they are carried forward in Section 4.

### 2. Footnote & Qualification Deep-Dive

- No footnote markers (`[^1]`, `*`, note references) appear in the supplied D001 evidence (pp. 1–3). There is therefore no footnote text to unpack or flag as missing in this capture.
- Qualification noted (not a footnote): p. 3 states "There were no material changes to the reporting entities during the reporting period, unless otherwise disclosed in the AFS." This is a scope qualification — consolidation boundary changes, if any, must be verified in the AFS (D003/D006), not assumed absent.
- Qualification noted: p. 3 states financial information is "consistent with the basis of preparation disclosed in the AFS" — the actual basis of preparation (IFRS, going concern, functional currency) is deferred to the AFS and must be checked there.
- Store count disclosure on p. 3 (358 stores = 316 Dis-Chem Pharmacy + 42 Baby City) is a point-in-time year-end figure with no comparative, no net-opening bridge, and no trading-space figure in this capture — these must be reconciled to the store portfolio table in the Analyst Presentation (D001 continuation, pp. 25–26) and the AFS.

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D001, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| N1 | High | D003 / D006 (AFS) | p. 3: "no material changes to the reporting entities … unless otherwise disclosed in the AFS" | Check AFS consolidation note for any acquisitions/disposals, new subsidiaries, or changes in consolidation in FY2026; confirm reporting boundary matches 358-store group | Consolidation changes distort like-for-like revenue and margin forecasts |
| N2 | High | D003 / D006 (AFS) | p. 3: basis of preparation deferred to AFS | Confirm functional/reporting currency (ZAR), going-concern statement, and any restatements in the AFS basis of preparation note | Currency and restatement risk affect all forecast inputs |
| N3 | Medium | D001 continuation (Analyst Presentation pp. 25–26) | p. 3: 358 stores (316 Dis-Chem + 42 Baby City) at year-end, no comparative or bridge | Reconcile to store portfolio table: opening count, net openings, closures/relocations, closing count, and trading space m² for both years | Store count and space drive sales and capex forecasts |
| N4 | Medium | D002 (CFO Report) / D003 | p. 3: retail operations "across South Africa, Namibia and Botswana" plus CJ Distribution wholesale | Confirm segmental revenue split (retail vs wholesale/CJ Distribution) and any cross-border currency exposure disclosure | Segment mix and FX affect margin and growth forecasts |

### 4. Updated Open Questions Ledger

```json
{"ledger_version": 1, "updates": [], "new_questions": [
  {"question": "Confirm in the AFS consolidation note whether there were any acquisitions, disposals, new subsidiaries, or changes in consolidation boundary in FY2026, and whether the reporting entity set matches the 358-store group described on D001 p.3.", "priority": "high", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D003 / D006 (AFS consolidation and basis of preparation notes)", "evidence_required": "AFS consolidation note listing subsidiaries and any FY2026 changes, with comparatives; explicit statement if no changes.", "closure_condition": "Consolidation boundary for FY2026 confirmed with note citation; any change quantified or explicit 'no change' stated; benign explanations (e.g., dormant entities) allowed."},
  {"question": "Confirm the AFS basis of preparation: functional and reporting currency (ZAR), going-concern statement, and whether any prior-year figures were restated or reclassified in FY2026.", "priority": "high", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D003 / D006 (AFS basis of preparation note)", "evidence_required": "Basis of preparation note text with currency, going-concern wording, and any restatement/reclassification disclosure with amounts.", "closure_condition": "Currency, going-concern status, and restatement position each confirmed with note citation; explicit statement if no restatements."},
  {"question": "Reconcile the year-end store count of 358 (316 Dis-Chem Pharmacy + 42 Baby City) stated on D001 p.3 to the store portfolio table: opening count, net openings, closures/relocations, closing count, and trading space m² for FY2026 vs FY2025.", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D001 continuation (Analyst Presentation pp. 25–26) / D005 Notes", "evidence_required": "Store portfolio table all rows/columns with units (stores, m²) for both dates, plus any footnotes.", "closure_condition": "Closing store count reconciles to 358 (or discrepancy quantified); net openings, closures and trading space extracted for both years with page citation."},
  {"question": "Confirm the segmental revenue split between retail pharmacy operations (South Africa, Namibia, Botswana) and CJ Distribution wholesale, and disclose any cross-border currency exposure, for FY2026 vs FY2025.", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D002 (CFO Report) / D003 (segmental note)", "evidence_required": "Segment revenue and profit table for retail vs wholesale, both years, in R'm, with any FX exposure disclosure.", "closure_condition": "Segment revenue split extracted for both years with page citation; FX exposure either quantified or explicit absence stated."}
]}
```

### 5. Baseline Forecast Inputs Captured Here

| Item | Value | Source |
| --- | --- | --- |
| Financial year-end | 28 February 2026 | [D001, p. 1; p. 3] |
| Reporting frameworks | IFRS, Integrated Reporting Framework, King V™, JSE Listings Requirements, Companies Act 71 of 2008 | [D001, p. 3] |
| Reporting boundary | Dis-Chem Pharmacies Limited and subsidiaries; SA, Namibia, Botswana retail + CJ Distribution wholesale | [D001, p. 3] |
| Total retail stores at year-end | 358 | [D001, p. 3] |
| — Dis-Chem Pharmacy stores | 316 | [D001, p. 3] |
| — Dis-Chem Baby City stores | 42 | [D001, p. 3] |
| Material changes to reporting entities | None disclosed (subject to AFS) | [D001, p. 3] |

### 6. Next Section to Capture

**D002 (Financial review, pp. 108–113 per map labels — CFO Report / financial review)** — it should address N4 (segment split) and provide the revenue, margin, debtor-cost and cash-flow figures needed before the primary statements (D003) and notes (D006). The store-portfolio reconciliation (N3) will require the D001 continuation capture of Analyst Presentation pp. 25–26.