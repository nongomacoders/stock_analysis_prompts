### 1. Answers to Stored Questions for This Section

- **Q-30355183667642da** (p.38 'PIC TO BE UPDATED' placeholder):
  - **Status**: `Partially resolved (remainder stays open for D001 continuation / D002)`
  - **Answer & evidence**: This capture confirms a second live placeholder: physical p.75 shows "76 Remuneration report / PIC TO BE UPDATED" as the entire page content `[D001, physical PDF p. 75]`. This is a distinct placeholder from the p.38 risk-section one and indicates the remuneration report page (printed p.76) was not populated in this interactive build. The p.38 risk-section completeness question remains open — no evidence here addresses it.

- **Q-65a1c0ff751b4c5e** (R07 residual rating / risk appetite):
  - **Status**: `Not addressed — carried forward` (no risk-register evidence in pp.73–76).

- **Q-9dcda868ba3541df** (revenue/total-income tables):
  - **Status**: `Not addressed — carried forward` (no revenue tables in this capture).

- **Q-2791af76c6484354** (store count 358 reconciliation):
  - **Status**: `Not addressed — carried forward` (no store portfolio table in this capture).

- **Q-17cae78f48974478** (p.25 footnote markers):
  - **Status**: `Not addressed — carried forward`.

- **Q-0386067925cb46f1 / Q-d8a9561a4c414bd7** (auditor's report / going concern):
  - **Status**: `Not addressed — carried forward` (auditor's report not in this capture).

- **Q-147d3b1800c14d55 / Q-96d9249b68ad4b03 / Q-d248d8f662874252 / Q-f7b17b6c14404ad1** (audit committee / committee compliance):
  - **Status**: `Partially resolved (remainder stays open for D002/D003)`
  - **Answer & evidence**: The Social and Ethics Committee report states it "confirms that it has executed its responsibilities per its terms of reference and applicable regulations. No material non-compliance with applicable regulations and legislation relating to the areas within the committee's mandate was brought to its attention… Dis-Chem incurred no material fines, penalties or convictions during the reporting period" `[D001, physical PDF p. 74]`. This is a self-certification by the SEC, not the Audit and Risk Committee; the audit committee report and JSE 5.7(h) statement remain unverified. Note the SEC composition on p.73 lists only three members (Sithebe, Coovadia, Masondo) — consistent with the p.63 "no longer a member" entries for Kobue and Saltzman, but effective resignation dates still not disclosed here.

### 2. Footnote & Qualification Deep-Dive

- **No footnote markers or footnote definitions appear in pp.73–76.** No `[^1]`, `*`, or note references are present in the supplied evidence; nothing to unpack or flag as missing.
- **p.75 placeholder qualification**: The page is effectively a section-divider stub reading "76 Remuneration report / PIC TO BE UPDATED" `[D001, physical PDF p. 75]`. This means the printed p.76 remuneration report content is absent from this build — any forecast input on executive incentive metrics (LTI/FSP vesting, STI payouts, share-based payment expense) cannot be sourced from here and must be checked in the remuneration implementation report (Part 3) and the AFS share-based payment note.
- **p.74 SEC self-certification**: "No material non-compliance… no material fines, penalties or convictions" is a management assertion with no quantified threshold for "material" — treat as unverified until cross-checked against the contingent liabilities/legal note in D006.
- **p.76 RemCo composition**: "75% of whom are independent" — with 4 NEDs shown (Mthimunye, Kobue, Masondo, Nestadt) plus Morais, this implies one non-independent NED; the independence classification is not footnoted here and should be checked against the directors' independence statement.
- **p.76 attendance table**: 13 March 2025 meeting shows CEO/CFO/Company Secretary as "N/A" (correctly excluded from own-remuneration discussion); 29 August 2025 shows Saltzman "N/A" — consistent with his departure, but the date is not stated.

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| N1 | High | D002 Financial review / D006 Notes | p.75 "PIC TO BE UPDATED" placeholder for printed p.76 remuneration report `[D001, p. 75]` | Confirm whether the remuneration report (Parts 1–3) is populated in the final report; if so, extract LTI/FSP scheme details, STI/LTI expense, and share-based payment expense FY2026 vs FY2025 | Share-based payment expense and dilution affect HEPS, EPS and cash flow; missing content blocks remuneration-linked forecast inputs |
| N2 | Medium | D006 Notes to the Financial Statements | SEC asserts "no material fines, penalties or convictions" `[D001, p. 74]` | Check contingent liabilities / legal proceedings note for any disclosed fines, penalties, or regulatory matters and their amounts | Unprovided liabilities could hit earnings; confirms or contradicts SEC assertion |
| N3 | Medium | D002 / D003 | RemCo "75% independent" with 4 NEDs listed `[D001, p. 76]` | Confirm NED independence classifications and which NED is non-independent; check directors' independence statement | Governance quality signal; affects confidence in capital allocation and remuneration discipline |
| N4 | Low | D001 continuation (p.63) / D002 | SEC composition reduced to 3 members; Saltzman "N/A" at 29 Aug 2025 meeting `[D001, pp. 73, 76]` | Obtain effective resignation dates for Kobue and Saltzman and any SEC recomposition disclosure | Completes Q-f7b17b6c14404ad1; governance completeness only, low forecast impact |
| N5 | Low | D002 / D006 | SEC FY2027 priorities include "finalising quantification of material ESG-related financial impacts… alignment with IFRS S1 and IFRS S2" `[D001, p. 74]` | Check whether any quantified ESG/climate financial impact or IFRS S1/S2 provision is disclosed in the financial review or notes | Potential future provisions/capex for climate transition; currently unquantified |

### 4. Updated Open Questions Ledger
```json
{"ledger_version": 1, "updates": [{"question_id": "Q-30355183667642da", "status": "partial", "answer": "A second 'PIC TO BE UPDATED' placeholder is confirmed on physical p.75, which is a stub for the printed p.76 remuneration report. The p.38 risk-section placeholder completeness question remains open; no evidence in pp.73-76 addresses it.", "evidence": [{"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 75, "quote": "76 Remuneration report\nPIC TO BE UPDATED"}]}, {"question_id": "Q-96d9240b68ad4b03", "status": "open", "answer": "", "evidence": []}, {"question_id": "Q-d248d8f662874252", "status": "partial", "answer": "No Audit and Risk Committee report or JSE 5.7(h) statement appears in pp.73-76. Only the SEC self-certification (p.74) is present; audit committee compliance and any internal control deficiencies remain unverified pending D002/D003.", "evidence": [{"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 74, "quote": "Dis-Chem incurred no material fines, penalties or convictions during the reporting period."}]}, {"question_id": "Q-f7b17b6c14404ad1", "status": "partial", "answer": "SEC composition on p.73 lists only Sithebe (Chair), Coovadia and Masondo, consistent with Kobue and Saltzman no longer being members; p.76 attendance shows Saltzman 'N/A' at the 29 August 2025 meeting. Effective resignation dates are still not disclosed in this capture.", "evidence": [{"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 73, "quote": "Alupheli Sithebe Independent Non-Executive Director BCom Acc, BAcc (Hons), CA(SA), MBA, The specific duties and oversight responsibilities of the committee include, but are not limited to, the"}, {"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 76, "quote": "29 August 2025 Present Present Present Present   Present Present  Present  N/A      Present"}]}], "new_questions": [{"question": "Confirm whether the remuneration report (Parts 1-3, printed p.76 onward) is populated in the final report or remains a 'PIC TO BE UPDATED' placeholder; if populated, extract LTI/FSP scheme terms, STI/LTI expense and share-based payment expense for FY2026 vs FY2025 in Rm.", "priority": "high", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D002 Financial review / D006 Notes", "evidence_required": "Remuneration implementation report (Part 3) text and tables; share-based payment note with FY2026 and FY2025 expense in Rm; explicit statement if content remains a placeholder.", "closure_condition": "Presence/absence of populated remuneration report confirmed with page citation; share-based payment expense both years extracted or confirmed absent."}, {"question": "Reconcile the Social and Ethics Committee assertion of 'no material fines, penalties or convictions' to the contingent liabilities and legal proceedings note; quantify any disclosed fines, penalties or regulatory matters.", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D006 Notes to the Financial Statements", "evidence_required": "Contingent liabilities/legal proceedings note text with amounts and page citation; explicit statement if none disclosed.", "closure_condition": "Any fines/penalties/legal matters quantified or confirmed absent with citation; SEC assertion reconciled or contradicted."}, {"question": "Confirm the independence classification of each Remuneration Committee NED and identify the non-independent member implied by the '75% independent' statement (4 NEDs listed).", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D002 / D003", "evidence_required": "Directors' independence statement or RemCo composition table with each NED's independence status and page citation.", "closure_condition": "Independence classification per NED confirmed with citation; 75% figure reconciled to member count."}, {"question": "Obtain effective resignation dates for Katlego Kobue and Saul Saltzman from the Social and Ethics Committee and any committee recomposition disclosure, reconciling to the 3-member SEC composition on p.73 and Saltzman 'N/A' at the 29 August 2025 meeting.", "priority": "low", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D001 continuation (p.63) / D002", "evidence_required": "Committee membership changes with effective dates and page citations.", "closure_condition": "Resignation dates and recomposition confirmed with citation."}, {"question": "Check whether any quantified ESG/climate-related financial impact or IFRS S1/S2 provision is disclosed, given the SEC FY2027 priority to 'finalise quantification of material ESG-related financial impacts'.", "priority": "low", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D002 Financial review / D006 Notes", "evidence_required": "Any ESG/climate financial impact quantification, provision or capex disclosure with amounts and page citation; explicit statement if none.", "closure_condition": "Presence/absence of quantified ESG financial impacts confirmed with citation; amounts extracted if present."}]}

```

### 5. Baseline Forecast Inputs Captured Here

| Item | Value | Source |
| --- | --- | --- |
| SEC meetings held FY2026 | 3 | `[D001, p. 73]` |
| SEC members | 3 (Sithebe Chair, Coovadia, Masondo) | `[D001, p. 73]` |
| RemCo meetings held FY26 | 3 | `[D001, p. 76]` |
| RemCo NEDs / independence | 4 NEDs listed; 75% independent | `[D001, p. 76]` |
| Material fines/penalties/convictions | Nil (SEC assertion) | `[D001, p. 74]` |
| Remuneration report content | Not populated — "PIC TO BE UPDATED" | `[D001, p. 75]` |

No revenue, margin, credit-book, store-count, lease, capex, HEPS or DPS figures appear in this capture.

### 6. Next Section to Capture

**D002 Financial review (physical pp.103–107)** — resolves Q-9dcda868ba3541df (revenue/total-income tables), Q-2791af76c6484354 (store count reconciliation), Q-0386067925cb46f1 / Q-d8a9561a4c414bd7 (auditor/going-concern cross-check), and N1 (remuneration/share-based payment expense).