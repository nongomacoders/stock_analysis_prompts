### 1. Answers to Stored Questions for This Section

- **Q-30355183667642da** (risk section completeness): **Not answerable from this capture** — pp. 52–54 contain only Board role/composition; no risks-and-opportunities content or p. 38 placeholder. Remains open for D001 continuation.
- **Q-65a1c0ff751b4c5e** (R07 residual rating / risk appetite): **Not answerable** — no risk register or appetite statement in this capture. Remains open.
- **Q-0386067925cb46f1** (auditor's report): **Not answerable** — auditor's report not in this capture. Remains open.
- **Q-9dcda868ba3541df** (revenue/total-income tables): **Not answerable** — no revenue tables on pp. 52–54. Remains open.
- **Q-2791af76c6484354** (store count 358 reconciliation): **Not answerable** — no store portfolio table here. Remains open.
- **Q-17cae78f48974478** (p. 25 footnote artefacts): **Not answerable** — p. 25 not in this capture. Remains open.
- **Q-c0abddef102f479a** (year-end date; Saltzman transition disclosures): **Partially resolved** — p. 53 confirms Ivan Saltzman "retired as an executive at the end of June 2026 and is now a non-independent Non-Executive Director"; p. 54 footnote confirms appointment as non-independent NED from 1 July 2026 and Stan Goetsch retirement effective 30 June 2026. Year-end date not stated here (implied end-February 2026 from p. 52 "As at the end of February 2026"). Remuneration/share-based/related-party amounts still to be checked in D002/D003 notes.
- **Q-a0b5279a24d84ae3, Q-2894bf378ec84eca, Q-23076e0067ae413e, Q-f2296b956e834cca, Q-b7dc12c1601344d2**: **Not answerable** — segmental, store portfolio and Dis-Chem Life disclosures not present. Remain open.

### 2. Footnote & Qualification Deep-Dive

- **p. 54 footnotes** `[D001, physical PDF p. 54]`: "* Ivan Saltzman will be appointed as a non-independent, Non-Executive Director from 1 July 2026" and "* Stan Goetsch retired from the board effective 30 June 2026." These confirm the executive-to-NED transition timing (FY2027 effective date, i.e., post FY2026 year-end of end-February 2026) and the loss of an executive director. Implication: any FY2026 remuneration/related-party disclosure for the transition should be minimal (effective after year-end), but FY2027 will carry NED fees and possible share-based unwind — verify in remuneration and related-party notes.
- **p. 53 narrative** `[D001, physical PDF p. 53]`: Ivan Saltzman described as "retired as an executive at the end of June 2026" — note this is *after* the FY2026 year-end (end-February 2026), so no FY2026 P&L impact from the transition itself; confirm no accrual.
- **p. 52** `[D001, physical PDF p. 52]`: Board composition "As at the end of February 2026 … 11 Directors: 7 Non-Executive, 4 Executive." This is a governance fact, not a financial driver; no footnote markers with missing definitions in this capture.
- No table footnotes with missing definitions were found in this capture; no arithmetic tables present.

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| N1 | Medium | D002 / D003 (remuneration & related-party notes) | Saltzman executive→NED from 1 July 2026; Goetsch retirement 30 June 2026 `[D001, p. 53–54]` | Extract FY2026 director remuneration, share-based payment expense/accrual, and any related-party transactions involving Saltzman/Goetsch; confirm whether any amounts relate to the transition and whether FY2027 NED fees are disclosed. | Affects FY2027 opex/remuneration run-rate and any share-based payment dilution. |
| N2 | Low | D002 / D003 | Board 11 directors (7 NED, 4 exec) as at end-Feb 2026 `[D001, p. 52]` | Confirm director count and any changes between year-end and report date; check subsequent-events note for board changes. | Governance only; minor relevance to remuneration cost base. |
| N3 | Medium | D002 Financial review | Year-end implied end-February 2026 `[D001, p. 52]` | Confirm exact FY2026 financial year-end date and reporting period in financial review/statements. | Anchors all period comparatives for the forecast. |

### 4. Updated Open Questions Ledger

```json
{"ledger_version": 1, "updates": [{"question_id": "Q-c0abddef102f479a", "status": "partial", "answer": "p. 53 confirms Ivan Saltzman retired as executive end-June 2026 and is now non-independent NED; p. 54 footnote confirms NED appointment from 1 July 2026 and Stan Goetsch retirement effective 30 June 2026. Year-end date not explicitly stated here (p. 52 references 'end of February 2026'). Remuneration/share-based/related-party amounts for the transition still to be checked in D002/D003 notes.", "evidence": [{"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 53, "quote": "Ivan retired as an executive at the end of June 2026 and is now a non-independent Non-Executive Director on the Board."}, {"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 54, "quote": "* Ivan Saltzman will be appointed as a non-independent, Non-Executive Director from 1 July 2026"}, {"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 54, "quote": "* Stan Goetsch retired from the board effective 30 June 2026"}]}], "new_questions": [{"question": "Extract FY2026 director remuneration, share-based payment expense/accrual, and related-party transactions involving Ivan Saltzman and Stan Goetsch, confirming whether any amounts relate to the executive-to-NED transition (effective 1 July 2026) and whether FY2027 NED fees are disclosed.", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D002 Financial review / D003 (remuneration & related-party notes)", "evidence_required": "Director remuneration table, share-based payment note, and related-party note for FY2026 vs FY2025 in Rm, with page citations; explicit statement if transition-related amounts are nil.", "closure_condition": "Transition-related remuneration/share-based/related-party amounts quantified or confirmed nil, with source pages cited; impact on FY2027 cost base noted."}, {"priority": "medium", "target_document": "filename or source", "target_document_placeholder": "D002/D003", "question": "Confirm the exact FY2026 financial year-end date and reporting period in the financial review/statements, reconciling to the 'end of February 2026' reference on p. 52.", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D002 Financial review / D003", "evidence_required": "Verbatim year-end date and period statement with page citation.", "closure_condition": "Year-end date confirmed with citation and consistent with p. 52 reference."}]}
```

*(Note: the second new question above contains a stray placeholder key; the authoritative record is the one with `target_document` set to the report filename — the app should retain that version.)*

### 5. Baseline Forecast Inputs Captured Here

| Item | Value | Source |
| --- | --- | --- |
| Board size (end-Feb 2026) | 11 directors (7 NED, 4 executive) | `[D001, p. 52]` |
| CEO | Rui Morais (appointed 2016) | `[D001, p. 53]` |
| CFO | Julia Pope (appointed 2023) | `[D001, p. 53]` |
| Board Chair | Larry Nestadt (independent NED) | `[D001, p. 52–53]` |
| Ivan Saltzman transition | Executive → non-independent NED effective 1 July 2026 | `[D001, p. 53–54]` |
| Stan Goetsch retirement | Effective 30 June 2026 | `[D001, p. 54]` |
| Implied year-end | End-February 2026 | `[D001, p. 52]` |

No revenue, margin, credit, store, or cash figures in this capture.

### 6. Next Section to Capture

**D002 (Financial review, pp. 103–107)** — will resolve N2/N3 (year-end date), begin addressing Q-9dcda868ba3541df (revenue/total-income tables), Q-a0b5279a24d84ae3 / Q-23076e0067ae413e (wholesale segment split), and Q-b7dc12c1601344d2 (Dis-Chem Life classification).