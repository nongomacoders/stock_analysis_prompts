### 1. Answers to Stored Questions

**Q-0cb... (D002/D003)** — Status: `Open (not addressed in D001)`. No revenue note present on pp. 19–21. Carry forward.

**Q-a0b5... (D002/D003)** — Status: `Open`. No segmental note present. Carry forward.

**Q-418d... (D002/D003)** — Status: `Open`. No category revenue table present. Carry forward.

**Q-3d91... (D002/D003)** — Status: `Partially resolved (remainder stays open for D002/D003)`. p. 21 confirms "Pharmacists, nurses, health advisers" as Human Capital inputs and "Nurse-led clinics and telehealth services" as an output, but no headcount, no trading-space split, no employee/occupancy cost figures. Remainder open.

**Q-ffa1... (D002/D003)** — Status: `Open`. Footnote [^22] not present in this capture. Carry forward.

**Q-56cf... (D002/D003)** — Status: `Open`. No Health Window quantification on pp. 19–21. Carry forward.

**Q-2307... (D002/D003)** — Status: `Open`. No wholesale revenue split present. Carry forward.

**Q-f229... (D002/D003)** — Status: `Open`. No store portfolio table present. Carry forward.

**Q-f480... (D002/D003)** — Status: `Open`. No category revenue table present. Carry forward.

**Q-0386... (D001 continuation / D003)** — Status: `Open`. Auditor's report not in this capture (pp. 19–21 are Overview/Business model). Carry forward.

**Q-2791... (D001 continuation / D005)** — Status: `Open`. Store count not restated here. Carry forward.

**Q-9dcd... (D001 continuation / D002)** — Status: `Open`. Revenue/total-income tables not present. Carry forward.

### 2. Footnote & Qualification Deep-Dive

- No footnote markers (`[^1]`, `*`, note refs) appear in the supplied pp. 19–21 evidence. No footnote text to unpack; no missing-footnote flag required for this capture.
- Two qualifications with forecast relevance:
  - p. 19: "The Group is not subject to any material litigation outside the ordinary course of business that is expected to have a material impact on its financial position or operations." — a negative assurance, not a quantified contingency. Verify against D003/D006 contingent liabilities note.
  - p. 19: "adjustments to the SEP and pharmacy dispensing fees" cited as a regulatory driver — no quantum given. Verify pricing/fee impact in D002.
  - p. 20: "Between FY2025 and FY2026, Dis-Chem's business model evolved from a predominantly retail pharmacy-led model to a more integrated, data-enabled healthcare ecosystem" — strategic narrative only; no revenue/margin attribution. Verify segmental split in D002/D003.
  - p. 21: "X, bigly labs" appears as the data-analytics/innovation entity name (likely OCR artefact of a brand name) — flag for confirmation of the correct entity name and any capitalised spend.

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section | Claim / anomaly / trigger | Specific verification instruction | Why it matters |
| --- | --- | --- | --- | --- | --- |
| N1 | High | D002 Financial review | p. 19 cites "adjustments to the SEP and pharmacy dispensing fees" as a regulatory driver with no quantum | Extract any disclosed dispensing-fee/SEP pricing impact on dispensary revenue and gross margin, FY2026 vs FY2025, Rm and % | Directly drives dispensary revenue and margin forecast |
| N2 | Medium | D002 / D003 | p. 20 claims business-model shift to "integrated, data-enabled healthcare ecosystem" FY2025→FY2026 | Quantify revenue/margin contribution of clinics, telehealth, Dis-Chem Health, Dis-Chem Life vs retail/wholesale; confirm segmental disclosure | Tests whether "diversification" is earnings-material or narrative |
| N3 | Medium | D003 / D006 | p. 19 negative assurance on litigation; p. 21 lists "Tax contributions" as output | Confirm contingent liabilities note and effective tax rate / tax paid, both years | Contingency and tax rate affect forecast EPS |
| N4 | Low | D002 / D006 | p. 21 "X, bigly labs" entity name (possible OCR artefact) | Confirm correct entity/brand name and any capitalised intangibles or opex for data/analytics | Confirms IP/intangibles and tech spend line |
| N5 | Medium | D002 / D003 | p. 21 lists "Better Rewards" loyalty and "Insurance policies" (Dis-Chem Life) as outputs | Extract loyalty/insurance revenue or cost if disclosed; confirm whether insurance underwriting sits in revenue or other income | Affects other-revenue and margin mix |

### 4. Updated Open Questions Ledger

```json
{"ledger_version": 1, "updates": [{"question_id": "Q-3d913094adfa45e6", "status": "partial", "answer": "D001 pp. 19-21 confirm health advisers and nurse-led clinics/telehealth as business-model inputs/outputs but disclose no adviser headcount, no category trading-space split, and no employee/occupancy cost figures. Remainder stays open for D002/D003.", "evidence": [{"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 21, "quote": "Pharmacists, nurses, health advisers, store teams, data scientists, and leadership"}, {"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 21, "quote": "Nurse-led clinics and telehealth services"}]}], "new_questions": [{"question": "Extract any disclosed financial impact of SEP adjustments and pharmacy dispensing-fee changes on dispensary revenue and gross margin for FY2026 vs FY2025 (Rm and %), with page citation; state explicitly if not quantified.", "priority": "high", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D002 Financial review", "evidence_required": "Dispensary revenue and margin figures both years, any regulatory pricing commentary with quantum, page citations.", "closure_condition": "Dispensing-fee/SEP impact quantified with period and source, or confirmed narrative-only; dispensary revenue and margin extracted both years."}, {"question": "Quantify the revenue and gross-margin contribution of clinics, telehealth, Dis-Chem Health and Dis-Chem Life versus retail and wholesale for FY2026 vs FY2025, and confirm the segmental disclosure that separates them.", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D002 / D003 (segmental note)", "evidence_required": "Segmental revenue and margin by service line, both years, Rm, with page citations; explicit statement if not separately disclosed.", "closure_condition": "Service-line contribution quantified or confirmed not separately disclosed; segmental note reconciled to group revenue."}, {"question": "Confirm the contingent liabilities note and the effective tax rate / tax paid for FY2026 vs FY2025, and reconcile to the p. 19 statement that no material litigation exists outside ordinary course.", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D003 / D006 (contingent liabilities and tax notes)", "evidence_required": "Contingent liabilities note, effective tax rate reconciliation, tax paid, both years, with page citations.", "closure_condition": "Contingent liabilities and tax rate extracted both years; consistency with p. 19 assurance confirmed or discrepancy flagged."}, {"question": "Confirm the correct entity/brand name behind the p. 21 reference 'X, bigly labs' (possible OCR artefact) and extract any capitalised intangibles or opex attributable to data/analytics/innovation for FY2026 vs FY2025.", "priority": "low", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D002 / D006 (intangible assets note)", "evidence_required": "Correct entity name with page citation; intangible assets and tech/innovation spend both years, Rm.", "closure_condition": "Entity name confirmed; related intangible/opex figures extracted or confirmed not separately disclosed."}, {"question": "Extract any disclosed revenue or cost for Better Rewards loyalty and Dis-Chem Life insurance, and confirm whether insurance underwriting profit/premiums sit in revenue or other income, FY2026 vs FY2025.", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D002 / D003 (revenue and other income notes)", "evidence_required": "Loyalty and insurance revenue/cost figures both years, Rm, classification (revenue vs other income), page citations.", "closure_condition": "Loyalty/insurance amounts and classification confirmed with citation, or explicit statement of non-disclosure."}]}
```

### 5. Baseline Forecast Inputs Captured Here

No hard financial figures (revenue, margin, debtor, store, capex, EPS, DPS) are printed on pp. 19–21. Only qualitative/structural facts:
- Business model: Retail & Wholesale Operations; Clinics & Telehealth; Digital Innovation & Data Analytics (p. 20).
- Six Capitals framework; King V™ governance reference (p. 20).
- Outputs listed: retail & wholesale revenue, healthcare consultations/prescriptions, loyalty participation, employment/skills, tax contributions, insurance policies (p. 21).
- No material litigation outside ordinary course (p. 19, negative assurance).
- Regulatory drivers named: Medicines and Related Substances Act, SAPC, DoH, Companies Act, JSE Listings Requirements; SEP and dispensing-fee adjustments (p. 19).

### 6. Next Section to Capture

**D002 Financial review (pp. 103–107)** — resolves N1, N2, N5 and stored Q-9dcd, Q-0cb0, Q-a0b5, Q-418d, Q-2307, Q-f480, Q-56cf, Q-ffa1 (revenue/category/segmental tables and margin bridge).