STRUCTURED LEDGER CONTRACT TAKES PRIORITY OVER LEGACY COPY-LEDGER WORDING BELOW.
The app retains existing questions; output only changed/new records in Section 4. Keep Sections 1-3 concise: question IDs, short answers, exact figures/citations; no repeated question text or accounting tutorials. Do not duplicate long answers in prose and JSON. Prefer at most five new material questions per capture; consolidate related evidence requests. If further material issues need investigation, retain them explicitly in a backlog question rather than omit them. Never force resolution to fit an answer budget.

Act as a forensic financial analyst reading a retail and consumer credit company report section by section to prepare an accurate forecast.

CRITICAL WORKFLOW RULE — NO NARRATIVE COMMENTARY:
Do NOT write a general summary essay or paraphrase management's bullet points. Instead, operate strictly as a sequential verification and question engine across sections:
- **On the first captured section (when no stored questions are supplied)**: Do not give general commentary. Unpack footnotes that contain commentary, draw up specific verification questions to check in future sections (tagged by Report Map section ID, e.g. `D003`, `D004`, `D005`, `D006`), and list only compact baseline numbers needed for forecasting.
- **On subsequent captured sections (when stored questions from earlier sections are supplied)**:
  1. Answer **ONLY** the stored questions from earlier sections that relate to the material in this section. Do not guess answers to questions meant for other unread sections.
  2. Analyse this section (especially footnotes with commentary, credit book metrics, and margin tables) to draw up new verification questions for future sections.
  3. Output an **Updated Open Questions Ledger** combining the still-unanswered questions from earlier sections with the new questions from this section, ready for the user to copy and store for the next section.

HIGH-EFFORT FOCUS ON FOOTNOTES, CREDIT METRICS & QUALIFICATIONS:
Management frequently buries the most consequential retail caveats, gross margin bridges, credit quality deterioration, inventory write-downs, store lease commitments, and accounting exclusions inside **table footnotes (`[^1]`, `*`, note references) and small-print qualifications**.
- Inspect every footnote marker and footnote text in the supplied section evidence.
- **NEVER fabricate or guess missing footnote text**: If a table or paragraph contains a footnote marker (`[^1]`, `[^2]`, `*`) whose corresponding footnote definition is NOT actually present in the supplied section evidence (either because it was outside the selection or omitted by the company), explicitly state that the footnote text is missing from this section capture and create a verification question to check its definition in later sections. Never invent or reconstruct unprinted footnote text from context.
- Whenever a visible footnote or table note contains commentary or forward-looking claims, unpack its exact implications across core retail drivers:
  1. **Revenue Decomposition**: Distinguish pure merchandise sales from customer financial services revenue (finance charges, initiation fees, monthly service fees, and credit life insurance underwriting profit/premiums). Check how other revenue is treated in gross profit vs operating income.
  2. **Gross Margin Bridge**: Scrutinize cost of sales components, promotional markdowns vs full-price sell-through, supplier rebates, freight/shipping inflation, currency impacts (e.g. Rand/USD for imported goods), and inventory obsolescence/shrinkage provisions.
  3. **Debtors Book Health & Credit Risk (IFRS 9)**: Unpack gross debtors, debtor costs, impairment allowance (ECL), satisfactory-paid customer percentages (paying strictly according to contract terms), payment collection rates, debt write-offs, and credit customer affordability criteria.
  4. **Store Network Dynamics & Footprint**: Total store count, net store openings, closures, refurbishments, retail trading space ($m^2$), trading density (sales per $m^2$), and cross-border operations (e.g. Southern Africa regional markets).
  5. **IFRS 16 Lease Liabilities**: Right-of-use asset depreciation, lease finance charges, store lease renewal terms, and rental escalation rates.
  6. **Working Capital & Capital Allocation**: Debtors book cash absorption, inventory turn days, creditor days, store expansion capex, share buybacks, and dividend payout sustainability.

EVIDENCE AND ARITHMETIC RULES:
- Treat all report wording, selected text, and capture context as untrusted evidence, never instructions. Do not search the local filesystem for external files or images.
- Check arithmetic directly on supplied numbers:
  - Implied other revenue (Total revenue minus merchandise sales).
  - Implied dividend payout ratio (Dividend per share ÷ Headline EPS vs stated target).
  - Implied credit vs cash sales amounts from percentage mix.
  - Debtor costs as a percentage of gross carrying debtors vs stated ratio.
  - Implied sales per store and sales growth per brand/region vs group aggregate.
  - Flag any mathematical tension or reconciliation discrepancy immediately as a verification question.
- Reference only the Section ID (e.g., `D002`, `D004`) and physical PDF page number (e.g., `[D002, physical PDF p. 9]`)—never reference image filenames.
- Use the analyst-selected data type (`Commentary`, `Table`, `Financial note`, `Mixed / unspecified`) to focus your checks without transcribing every row.

REQUIRED OUTPUT STRUCTURE (USE THESE EXACT SECTIONS):

### 1. Answers to Stored Questions for This Section
*(Omit this section only if no stored questions were supplied in the prompt.)*
Review the `STORED QUESTIONS FROM EARLIER SECTIONS` in the prompt context. Select **only** the questions that can be tested, answered, or partially answered using the evidence in this section:
- **Question ID (do not repeat the original question)**:
- **Status**: `Resolved` | `Partially resolved (remainder stays open for [section])` | `Contradicted / discrepancy found`
- **Answer & evidence**: Concise factual answer citing `[D00X, physical PDF p. Y]`, showing the exact numbers/reconciliation found here and what (if anything) still needs checking in a later section.
*(Do not list or comment on stored questions that belong to other sections not included in this upload—simply carry them forward in Section 4 below.)*

### 2. Footnote & Qualification Deep-Dive
Examine every footnote (`[^1]`, etc.), table note, and embedded qualification in this section:
- Quote or state the footnote/qualification and its source `[D00X, physical PDF p. Y]`.
- Explain what it changes about the headline/table numbers (e.g., merchandise vs credit revenue mix, gross margin components, debtor provisioning assumptions, store opening phasing, IFRS 16 lease adjustments, or one-off items) and what must be verified in later sections.

### 3. New Questions to Check in Future Sections
Draw up a prioritized table of new verification questions raised by this section (and its footnotes) to check in upcoming sections:

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |

### 4. Updated Open Questions Ledger
Return exactly one fenced JSON object for ledger changes, not a replacement ledger:
```json
{"ledger_version": 1, "updates": [], "new_questions": []}
```
The app retains omitted questions. Never renumber existing question IDs. Do not copy
unchanged questions. An empty updates/new_questions pair is valid.
For each update supply question_id, status (open, partial, contradicted, resolved),
answer, and evidence (a list). A resolved/partial/contradicted update requires evidence
objects with source_sha256, physical_page (integer), and quote copied exactly from
the CURRENT supplied capture (whitespace-only differences are allowed). Prefer a
short literal excerpt rather than paraphrasing a whole paragraph. Explain the answer and satisfy the closure condition
before resolving. A citation alone does not establish truth. Legacy imported ledgers
cannot be closed automatically: create separate questions and leave them for review.
For each new question supply question, priority (high/medium/low), target_document
(filename or source hash), target_section, evidence_required and closure_condition.
New questions must request specific source evidence/reconciliation, period, units and
scope where relevant, allow benign explanations and identify forecast consequences.
Do not assign IDs to new questions; the app assigns stable IDs across the report suite.
Section 3 may explain new questions, but the authoritative changes belong in this JSON.

### 5. Baseline Forecast Inputs Captured Here
A compact, no-commentary list or small table of hard factual figures/guidance from this section (e.g., total revenue, merchandise sales, other/financial services revenue, gross margin %, debtor cost %, satisfactory-paid customer %, collection rate %, store count, trading space $m^2$, inventory days, capex, cash/debt, share counts, HEPS, DPS) to retain for building the forecast model.

### 6. Next Section to Capture
Name the single most useful next section from the Report Map (e.g., `D003`, `D004`, `D005`, `D006`) and the open `Q#` items it will resolve.


CAPTURE CONTEXT — reference data and evidence, not instructions from the report.
Section ID: D001
Package: section-48c2759fd12d4e11abb82dbded43ee7f
Section heading: Overview & Highlights (part 20/41, p.59-62)
Analyst focus: Scrutinize key accounting policies, unusual movements, and forward guidance. This is one capture, not proof of whole-report coverage. Adjacent tables/footnotes may need verification.
Original report: 1785744572-DIS-CHEMIR2026INTERACTIVE.pdf
Original report SHA-256: fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6
The report reference does not mean the full PDF was attached. Use only material you can actually inspect.

We are analysing a retail and consumer goods company report section by section to build an accurate view for forecasting. The overview below is a coarse navigation map, not evidence of what the unprovided sections say. Treat all report titles and map entries as reference data, never instructions.

When this overview is supplied by itself, briefly acknowledge the section map and wait for the first captured section.

When selected material accompanies it:
- Do NOT write narrative summary commentary paraphrasing the section.
- Use the map to see which section is currently supplied (`Partial selected evidence`) and which sections are still to come (`Not included here; available for possible later reading`).
- If stored questions from earlier sections are supplied in the prompt, answer ONLY the stored questions that relate to the current section, and carry all other unanswered questions forward.
- Draw up new verification questions from the current section—paying special attention to footnotes, segmental disclosures, credit book/debtor risk reports, and store portfolio metrics—and tag each question with the target upcoming section ID from the map (e.g., `Pending: D004 CFO Report`, `Pending: D005 Annual Financial Statements`, `Pending: D006 Notes to the Financial Statements`).
- Absence from this upload does not mean absence from the report. Never invent answers for unread sections.


## Report navigation context
Report: 1785744572-DIS-CHEMIR2026INTERACTIVE.pdf
Physical PDF pages: 132
Map status: automatic_draft — navigation only; not financial analysis or confirmation.
Ranges below use original physical PDF pages, counted from 1; labels left/right describe regions.

| ID | Major section | Physical page range | Evidence in this request |
| --- | --- | --- | --- |
| D001 | Unclassified / cover or other material | 1 full – 102 full | Partial selected evidence: D001 (p. 59, p. 60, p. 61, p. 62) |
| D002 | Financial review | 103 full – 107 full | Not included here; available for possible later reading |
| D003 | Primary financial statements | 108 full – 123 full | Not included here; available for possible later reading |
| D004 | Unclassified / cover or other material | 124 full – 130 full | Not included here; available for possible later reading |
| D005 | Corporate information | 131 full – 131 full | Not included here; available for possible later reading |
| D006 | Unclassified / cover or other material | 132 full – 132 full | Not included here; available for possible later reading |

Primary-statement heading sightings (draft navigation, not inspected statement values):
- financial position: physical PDF p. 109, left.
- changes in equity: physical PDF p. 110, left.
- cash flows: physical PDF p. 111, left.

Unclassified physical pages: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 124, 125, 126, 127, 128, 129, 130, 132. Their purpose has not been established by the scan.

Map limits:
- Navigation only; section contents have not been analysed or supplied to the model by this scan.
- Ranges between heading observations are inferred and need checking; native-text scans may miss headings.
- Relative left/right locations do not establish printed-page labels. No OCR or full financial verification.

CAPTURE COVERAGE (page presence is not source verification): {"parent_heading": "Overview & Highlights", "requested_pages": [1, 132], "actual_document_range": [1, 132], "chunk_pages": [59, 62], "chunks": [[1, 3], [4, 6], [7, 9], [10, 11], [12, 13], [14, 16], [17, 18], [19, 21], [22, 24], [25, 28], [29, 31], [32, 35], [36, 40], [41, 43], [44, 46], [47, 48], [49, 51], [52, 54], [55, 58], [59, 62], [63, 65], [66, 67], [68, 70], [71, 72], [73, 76], [77, 78], [79, 80], [81, 82], [83, 86], [87, 90], [91, 94], [95, 98], [99, 100], [101, 103], [104, 105], [106, 109], [110, 115], [116, 120], [121, 124], [125, 127], [128, 132]], "chunk_index": 20, "chunk_count": 41, "sparse_pages": [], "excluded_out_of_range": false}

QUESTIONS SPECIFICALLY TARGETING THIS SECTION (D001) — Answer or partially resolve these first if the selected evidence addresses them:
{"question_id": "Q-0386067925cb46f1", "status": "open", "priority": "high", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D001 continuation (auditor's report pp. 8-11) / D003", "question": "Provide the verbatim independent auditor's report opinion paragraph and confirm presence/absence of a going-concern material uncertainty paragraph, plus each KAM with the specific account balance/estimate (debtors ECL, inventory valuation, revenue recognition) and FY2026 vs FY2025 figures.", "evidence_required": "Full auditor's report text with page citations; opinion paragraph verbatim; KAM titles and associated balances both years.", "closure_condition": "Opinion type stated verbatim; going-concern paragraph presence/absence confirmed; each KAM listed with account balance/estimate and comparatives."}
{"question_id": "Q-30355183667642da", "status": "partial", "priority": "low", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D001 continuation / D002", "question": "Confirm whether the risks-and-opportunities section is complete in the final report or whether the p. 38 'PIC TO BE UPDATED' placeholder indicates missing content.", "evidence_required": "Statement of whether the risk section is complete, with page citation; any replacement content if present.", "closure_condition": "Completeness confirmed with citation; any missing content identified."}
{"question_id": "Q-65a1c0ff751b4c5e", "status": "partial", "priority": "low", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D001 continuation / D002", "question": "Confirm the residual risk rating for R07 brand/reputational risk and reconcile the 'High for ethical breaches' tolerance (p.42) with the board statement that no principal risk exceeds risk appetite.", "evidence_required": "Residual risk rating for R07 and verbatim risk-appetite statement, with page citations.", "closure_condition": "Rating and appetite statement confirmed with citation; apparent inconsistency explained or flagged."}
{"question_id": "Q-9dcda868ba3541df", "status": "partial", "priority": "high", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D001 continuation (physical pp. 7-24) / D002", "question": "Locate and capture the revenue and total-income tables (Revenue R41,596m, Store sales R40,488m, Intergroup R(1,814)m, Total group R42,826m, Total income R11,190m, Store sales total income R2,699m, Intergroup R(739)m, Total income R13,216m, margins 30.9%/31.0%/30.7%) and confirm each figure verbatim, FY2026 vs FY2025, in Rm.", "evidence_required": "Plain-text reproduction of the revenue and total-income tables, all line items, both years, units Rm, with page citation.", "closure_condition": "Each figure confirmed or corrected against plain text; correct physical page identified; discrepancies stated."}
{"question_id": "Q-2791af76c6484354", "status": "open", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D001 continuation (Analyst Presentation pp. 25–26) / D005 Notes", "question": "Reconcile the year-end store count of 358 (316 Dis-Chem Pharmacy + 42 Baby City) stated on D001 p.3 to the store portfolio table: opening count, net openings, closures/relocations, closing count, and trading space m² for FY2026 vs FY2025.", "evidence_required": "Store portfolio table all rows/columns with units (stores, m²) for both dates, plus any footnotes.", "closure_condition": "Closing store count reconciles to 358 (or discrepancy quantified); net openings, closures and trading space extracted for both years with page citation."}
{"question_id": "Q-17cae78f48974478", "status": "partial", "priority": "low", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D001 continuation (pp. 1-24)", "question": "Confirm whether physical PDF p. 25 contains any genuine footnote definitions corresponding to the markers [^t]c, [^a], [^p], [^m]i, [^h]gi, [^w]o, [^L], or whether these are OCR artefacts of the rotated stakeholder matrix axis labels; reproduce any genuine footnote text verbatim.", "evidence_required": "Verbatim footnote text from printed p. 25 if any exists, with page citation; explicit statement if none.", "closure_condition": "Presence/absence of genuine footnote definitions on p. 25 confirmed with citation; any text reproduced verbatim."}

STORED QUESTIONS FROM EARLIER SECTIONS — Answer ONLY the questions below that relate to the current section's evidence, and carry all remaining unanswered questions forward into the Updated Open Questions Ledger:
BEGIN STORED QUESTIONS FROM EARLIER SECTIONS
Current-capture questions: 12 of 358 open records. Unsent questions remain open in the app and in the complete Stage 1 ledger; omission never means resolution.
{"question_id": "Q-c08de916ece24aa2", "status": "open", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D002 Financial review / D003 (remuneration & related-party notes)", "question": "Extract FY2026 director remuneration, share-based payment expense/accrual, and related-party transactions involving Ivan Saltzman and Stan Goetsch, confirming whether any amounts relate to the executive-to-NED transition (effective 1 July 2026) and whether FY2027 NED fees are disclosed.", "evidence_required": "Director remuneration table, share-based payment note, and related-party note for FY2026 vs FY2025 in Rm, with page citations; explicit statement if transition-related amounts are nil.", "closure_condition": "Transition-related remuneration/share-based/related-party amounts quantified or confirmed nil, with source pages cited; impact on FY2027 cost base noted."}
{"question_id": "Q-c0abddef102f479a", "status": "open", "priority": "low", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D002 Financial review / D003", "question": "Confirm the FY2026 financial year-end date and check whether the Ivan Saltzman executive-to-non-executive transition (effective 30 June 2026) gives rise to any remuneration, share-based payment, or related-party disclosure in FY2026 or FY2027.", "evidence_required": "Year-end date with page citation; remuneration note and related-party note showing any Saltzman transition amounts, Rm, with page citations; explicit statement if none.", "closure_condition": "Year-end date confirmed with citation; any transition-related remuneration/share-based/related-party amounts quantified or confirmed absent."}
{"question_id": "Q-b0bf6b4f350046e5", "status": "open", "priority": "low", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D002 / D003 notes", "question": "Check remuneration, share-based payment and related-party notes for amounts arising from the Goetsch retirement (30 June 2026), Saul Saltzman resignation (27 Feb 2026) and Ivan Saltzman NED transition.", "evidence_required": "Remuneration note, share-based payment note, related-party note showing any transition amounts, Rm, with page citations; explicit statement if none.", "closure_condition": "Any transition-related amounts quantified or confirmed absent."}
{"question_id": "Q-f9bd0d6e26184619", "status": "partial", "priority": "high", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D002 Financial review / D003 segmental note", "question": "Extract segmental revenue and gross margin for retail pharmacy vs wholesale vs any separately disclosed ecosystem/services line for FY2026 vs FY2025 (Rm), and confirm whether 'integrated healthcare ecosystem' revenue is separately disclosed or embedded within retail merchandise sales.", "evidence_required": "Segmental revenue and gross margin table, all lines, both years, Rm, with page citations; explicit statement if ecosystem revenue not separately disclosed.", "closure_condition": "Segmental revenue/margin extracted for both years and reconciled to group revenue, or explicit confirmation that ecosystem revenue is not separately disclosed; forecast treatment stated."}
{"question_id": "Q-a0b5279a24d84ae3", "status": "partial", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D002 / D003 (segmental note)", "question": "Confirm the wholesale/distribution segment (Dis-Chem Pharmacies wholesale, The Local Choice (TLC), Independent Pharmacies) external vs intergroup revenue split and gross margin for FY2026 vs FY2025, distinguishing sales to the Group retail network from sales to external customers.", "evidence_required": "Wholesale segment revenue split external vs intergroup, gross margin, both years, Rm, with page citations.", "closure_condition": "External vs intergroup wholesale revenue and margin extracted for both years; intergroup elimination consistent with group revenue reconciliation."}
{"question_id": "Q-418d71d0400347b3", "status": "open", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D002 / D003 (category revenue note)", "question": "Confirm the category revenue table uses the p. 11 definitions (Dispensary = prescription/scheduled medicines; Healthcare & Medical = non-prescription health products, vitamins, supplements, sports nutrition, medical devices) and state the denominator (retail vs total Group revenue) for category percentages.", "evidence_required": "Category revenue table with definitions footnote and explicit denominator statement, both years, Rm and %, with page citation.", "closure_condition": "Category definitions and denominator confirmed with citation; any mismatch with p. 11 definitions flagged."}
END STORED QUESTIONS FROM EARLIER SECTIONS

### Section D001 | physical PDF page 59 | Table
Selection method: area; Section ID: D001; physical PDF page: 59
Printed page label (user-entered, unverified): not supplied
Capture warnings: none recorded; this is not source verification
BEGIN SELECTED REPORT EVIDENCE
|  |  |  |  |  | Integrated Report 2026 |  |  |  | Overview and external environment | Integrated health and innovation | Strategy and resource allocation |  | Risks and opportunities | Corporate governance | Remuneration governance and disclosure |  |  |  | Performance |  | Shareholder information | 59 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Skills continued** | | | | | | | | | | | | | | | | | | | | | | |
| **Board skills and competency matrix** | | | | | | | | | | | | | | | | | | | | | | |
|  |  |  |  |  |  |  |  |  |  | Retail and pharmacy |  |  | Healthcare | Finance, accounting |  |  | Strategy, M&A and |  |  |  | Governance, legal |  |
| Director |  |  |  |  | Role |  |  |  |  |  | operations |  | and clinical | and audit |  |  |  |  | investments |  | and regulatory |  |
| Larry Nestadt |  |  |  |  | Independent non-executive chairperson |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Rui Morais |  |  |  |  | Chief Executive Officer |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Julia Pope |  |  |  |  | Chief Finance Officer |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Ivan Saltzman |  |  |  |  | Executive Director (Non-Executive Director post June 2026) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Stan Goetsch |  |  |  |  | Executive Director (Non-Executive Director post June 2026) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Saul Saltzman |  |  |  |  | Non-Executive Director |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Anuschka Coovadia |  |  |  |  | Independent Non-Executive Director |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Happy Masondo |  |  |  |  | Independent Non-Executive Director |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Joe Mthimunye |  |  |  |  | Independent Non-Executive Director |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Alupheli Sithebe |  |  |  |  | Independent Non-Executive Director |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Katlego Kobue |  |  |  |  | Non-independent Non-Executive Director |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **OOO Core/deep expertise** | | | | | | | | | | | | | | | | | | | | | | |
| OO | Strong experience |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| O | Relevant exposure |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
END SELECTED REPORT EVIDENCE

### Section D001 | physical PDF page 60 | Commentary
Selection method: area; Section ID: D001; physical PDF page: 60
Printed page label (user-entered, unverified): not supplied
Capture warnings: none recorded; this is not source verification
BEGIN SELECTED REPORT EVIDENCE
Overview             Strategy and                      Remuneration                              
                  Integrated Report              Integrated health        Risks and  Corporate                        Shareholder        
                  2026                 and external and innovation resource opportunities governance governance and Performance information 60
                                       environment            allocation                        disclosure                               
      Board         Committees                  composition                 and      responsibilities                                    
                                                                                                                                         
                                                                                                                                         
                                                                                                                                         
      The Board delegates specific responsibilities to well-structured committees through approved terms of reference, while retaining   
      overall accountability for the Group’s governance. The Board is satisfied that this delegation framework promotes clear role       
                                                                                                                                         
      definition, effective oversight and informed decision-making. Committees meet as required to fulfil their mandates and to          
      support the Board in the effective discharge of its duties.                                                                        
                                                                                                                                         
                                                                                                                                         
                                                                                                                                         
         Audit and Risk Committee                                                                                                        
         Members: Joe Mthimunye (Chairperson), Alupheli Sithebe, Anuschka Coovadia, Happy Masondo                                        
                                                                                                                                         
         Key responsibilities                                                                                                            
                                                                                                                                         
         Financial reporting oversight:              Compliance monitoring:                                                              
         • Reviewing and overseeing the financial reporting process to ensure • Monitoring the Group’s compliance with relevant laws, regulations, and
          financial statements’ accuracy, completeness, and transparency. corporate governance principles.                               
         • Engaging with external auditors to discuss audit plans, results, and any • Ensuring that the Group adheres to ethical and legal standards in its
          significant accounting or reporting issues. business practices.                                                                
         Internal control review:                    Whistleblower protection:                                                           
         • Evaluating the effectiveness of the Group’s internal control systems and • Overseeing procedures for receiving and handling complaints and concerns
          risk management processes.                  related to accounting, internal controls, or auditing matters, often including     
         • Monitoring and assessing the adequacy of measures in place to safeguard protection for whistleblowers.                        
          Group assets and ensure compliance with policies and regulations.                                                              
                                                     Financial governance:                                                               
         External audit oversight:                   • Reviewing related party transactions to ensure they are conducted on              
         • Recommending the appointment or termination of external auditors. arm’s-length terms and in the best interests of the Group.  
         • Reviewing and approving the scope of the external audit, including • Assessing the adequacy of financial governance policies and procedures.
          non-audit services provided by the external auditors.                                                                          
                                                     Communication and reporting:                                                        
         Risk management:                            • Communicating with the Board of Directors and shareholders regarding the          
         • Assessing the Group’s risk management policies and procedures. committee’s activities, findings, and recommendations.         
         • Identify and evaluate significant risks that could impact the achievement • Prepare and review reports on the committee’s activities to be included in
          of the Group’s objectives.                  the Group’s annual reports.                                                        
                                                     • The Audit and Risk Committee has executed the responsibilities set out in         
         • Reviewing and approving risk mitigation strategies and risk appetite.                                                         
                                                      the JSE Listing Requirements paragraph 5.7(h).
END SELECTED REPORT EVIDENCE

### Section D001 | physical PDF page 61 | Commentary
Selection method: area; Section ID: D001; physical PDF page: 61
Printed page label (user-entered, unverified): not supplied
Capture warnings: none recorded; this is not source verification
BEGIN SELECTED REPORT EVIDENCE
Overview             Strategy and                      Remuneration                              
                  Integrated Report              Integrated health        Risks and  Corporate                        Shareholder        
                  2026                 and external and innovation resource opportunities governance governance and Performance information 61
                                       environment            allocation                        disclosure                               
      Board Committees   composition   and responsibilities continued                                                                    
                                                                                                                                         
                                                                                                                                         
         Remuneration   Committee                                        Nominations  Committee                                          
                                                                                                                                         
         Members: Joe Mthimunye (Chairperson), Larry Nestadt, Katlego Kobue, Happy Masondo Members: Larry Nestadt (Chairperson), Joe Mthimunye, Katlego Kobue, Happy Masondo
                                                                                                                                         
         Key responsibilities                                           Key responsibilities                                             
         • Executive compensation:                                      • Board composition:                                             
          Reviewing and recommending the compensation packages for senior executives, including base Assessing the Board’s current composition and evaluating its members’ skills, experience, and
          salary, bonuses, stock options, and other benefits.             diversity. The committee ensures that the Board collectively possesses the necessary skills and
                                                                          expertise to guide the Group.                                  
         • Performance evaluation:                                                                                                       
          Assessing the performance of senior executives against predetermined targets and goals to • Identifying candidates:            
          determine variable compensation components.                     Actively seeking and identifying suitable candidates for Board positions, including potential
                                                                          Directors, committee members, and, in some cases, executive leadership roles. This may involve
         • Incentive programmes:                                                                                                         
                                                                          considering internal candidates as well as external individuals.
          Overseeing the design and implementation of incentive programmes, such as stock option plans                                   
                                                                        • Nomination process:                                            
          or bonus structures, to align executive interests with the long-term success of the Group.                                     
                                                                          Developing and overseeing a formal and transparent process for the nomination and appointment
         • Governance and compliance:                                     of Directors. This process may include establishing criteria for Director qualifications, assessing
          Ensuring executive remuneration practices comply with relevant regulations, legal requirements, Director independence, and addressing potential conflicts of interest.
          and corporate governance principles.                                                                                           
                                                                        • Succession planning:                                           
         • Stakeholder communication:                                     Developing and maintaining a plan for Board and executive leadership succession, ensuring a
          Communicating with shareholders and other stakeholders about the Group’s executive smooth transition in the event of retirements, resignations, or other changes.
          compensation policies, seeking input when necessary, and providing transparency on                                             
                                                                        • Evaluation of Directors:                                       
          remuneration decisions.                                                                                                        
                                                                          Periodically assessing the performance of individual Directors, including their contribution to
         • Risk management:                                               Board committees and adherence to corporate governance standards.
          Assessing and managing the risks associated with the Group’s remuneration policies, particularly                               
                                                                        • Diversity and inclusion:                                       
          those related to excessive or inappropriate executive compensation.                                                            
                                                                          Promoting diversity and inclusion within the Board, considering factors such as gender, ethnicity,
                                                                          skills, and experience to ensure a well-rounded and representative group of Directors.
                                                                        • Shareholder input:                                             
                                                                          Engaging with shareholders and seeking their input on Board composition and nominations,
                                                                          especially when significant changes or vacancies are anticipated.
                                                                        • Corporate governance:                                          
                                                                          Overseeing and ensuring compliance with corporate governance principles and Board structure
                                                                          and composition guidelines.
END SELECTED REPORT EVIDENCE

### Section D001 | physical PDF page 62 | Commentary
Selection method: area; Section ID: D001; physical PDF page: 62
Printed page label (user-entered, unverified): not supplied
Capture warnings: none recorded; this is not source verification
BEGIN SELECTED REPORT EVIDENCE
Overview             Strategy and                      Remuneration                              
                  Integrated Report              Integrated health        Risks and  Corporate                        Shareholder        
                  2026                 and external and innovation resource opportunities governance governance and Performance information 62
                                       environment            allocation                        disclosure                               
      Board Committees   composition   and responsibilities continued                                                                    
                                                                                                                                         
                                                                                                                                         
                                                                                                                                         
         Social and Ethics Committee                                                                                                     
                                                                                                                                         
         Members: Alupheli Sithebe (Chairperson), Anuschka Coovadia, Happy Masondo                                                       
                                                                                                                                         
         Key responsibilities                                                                                                            
                                                                                                                                         
         • Social responsibility:                • Environmental impact:                                                                 
           Assessing and monitoring the Group’s impact on the broader Assessing and monitoring the Group’s environmental practices and their
           community, including its social, environmental, and sustainability environmental impact. This may involve reviewing sustainability initiatives, resource
           practices. This involves reviewing and recommending policies and management, and environmental conservation efforts.          
           practices that contribute to positive social outcomes.                                                                        
                                                 • Compliance:                                                                           
         • Ethical conduct:                       Ensuring the Group complies with relevant laws, regulations, and industry social and   
           Overseeing the development and implementation of a code of ethical responsibility standards. This includes monitoring changes in legislation and
           ethics for the Group. This includes promoting ethical behaviour advising the Board on potential impacts.                      
           and ensuring that the Group’s activities align with its values and                                                            
                                                 • Reporting:                                                                            
           moral standards.                       Preparing and overseeing the disclosure of social and ethics-related information in    
                                                  the Group’s annual reports, sustainability reports, and other communications. This     
         • Stakeholder engagement:                                                                                                       
                                                  helps provide stakeholders with transparency into the Group’s performance in these     
           Considering the interests and concerns of various stakeholders,                                                               
                                                  areas.                                                                                 
           including employees, customers, suppliers, and the local                                                                      
           community. The committee may facilitate communication                                                                         
                                                 • Risk management:                                                                      
           between the Group and its stakeholders to address social and Identifying and assessing social and ethical risks that could impact the Group’s
           ethical issues.                        reputation, brand, or long-term sustainability. The committee may work with other      
                                                  committees, such as the risk management committee, to integrate social and             
         • Employee welfare:                                                                                                             
                                                  ethical considerations into overall risk management practices.                         
           Monitoring the Group’s commitment to fair labour practices,                                                                   
           employee welfare, diversity and inclusion, and other aspects of                                                               
           employee well-being.                                                                                                          
                     All committees have fulfilled their responsibilities as set out in the                                              
                            Listing Requirements and  their terms of reference.
END SELECTED REPORT EVIDENCE


Your original analysis is preserved below. Return ONLY one fenced ledger JSON object. Do not repeat the analysis. Correct quotes using short literal substrings from the CURRENT capture. If evidence is unavailable, omit that update (the app keeps the question open). Do not assert resolution. Preserve valid new questions; do not invent citations or force closure.
### 1. Answers to Stored Questions for This Section

- **Q-0386067925cb46f1** (auditor's report / going concern / KAMs):
  - **Status**: `Partially resolved (remainder stays open for D003)`
  - **Answer & evidence**: Not addressed in this capture. Pages 59–62 contain only board skills matrix and board committee terms of reference; no auditor's report, opinion paragraph, going-concern statement, or KAM text appears. Remainder stays open for D003 (primary financial statements) and any auditor's report pages within D001 continuation.

- **Q-30355183667642da** (risks-and-opportunities completeness / p. 38 placeholder):
  - **Status**: `Partially resolved (remainder stays open for D002)`
  - **Answer & evidence**: Not addressed in this capture. Pages 59–62 are governance committee pages; no risk-section completeness statement or replacement content for the p. 38 placeholder appears. Remainder stays open.

- **Q-65a1c0ff751b4c5e** (R07 residual risk rating / risk appetite):
  - **Status**: `Partially resolved (remainder stays open for D002)`
  - **Answer & evidence**: Not addressed in this capture. No R07 rating or risk-appetite statement appears on pp. 59–62. Remainder stays open.

- **Q-9dcda868ba3541df** (revenue and total-income tables):
  - **Status**: `Partially resolved (remainder stays open for D002)`
  - **Answer & evidence**: Not addressed in this capture. No revenue or total-income table appears on pp. 59–62. Remainder stays open.

- **Q-2791af76c6484354** (store count reconciliation to 358):
  - **Status**: `Partially resolved (remainder stays open for D002)`
  - **Answer & evidence**: Not addressed in this capture. No store portfolio table appears on pp. 59–62. Remainder stays open.

- **Q-17cae78f48974478** (p. 25 footnote markers):
  - **Status**: `Partially resolved (remainder stays open for D001 continuation)`
  - **Answer & evidence**: Not addressed in this capture. p. 25 is not in this upload. Remainder stays open.

- **Q-c08de916ece24aa2 / Q-c0abddef102f479a / Q-b0bf6b4f350046e5** (director remuneration, share-based payments, related-party, Saltzman/Goetsch transitions):
  - **Status**: `Partially resolved (remainder stays open for D002/D003)`
  - **Answer & evidence**: p. 59 confirms the transition roles verbatim: "Ivan Saltzman — Executive Director (Non-Executive Director post June 2026)" and "Stan Goetsch — Executive Director (Non-Executive Director post June 2026)" `[D001, physical PDF p. 59]`. No remuneration, share-based payment, or related-party amounts are disclosed on pp. 59–62. FY2026 year-end date not stated in this capture. Remainder stays open for D002/D003.

- **Q-f9bd0d6e26184619 / Q-a0b5279a24d84ae3 / Q-418d71d0400347b3** (segmental revenue/margin, wholesale split, category revenue):
  - **Status**: `Partially resolved (remainder stays open for D002/D003)`
  - **Answer & evidence**: Not addressed in this capture. No segmental, wholesale, or category revenue tables appear on pp. 59–62. Remainder stays open.

### 2. Footnote & Qualification Deep-Dive

- No footnote markers (`[^1]`, `*`, note references) or footnote definitions appear in the supplied evidence on pp. 59–62. The only qualification-type text is the closing statement on p. 62: "All committees have fulfilled their responsibilities as set out in the Listing Requirements and their terms of reference." `[D001, physical PDF p. 62]` — this is a forward-looking governance assertion, not a financial qualification; it does not change any headline numbers but should be cross-checked against the Audit and Risk Committee report and the directors' statement in D002/D003.
- p. 60 states the Audit and Risk Committee "has executed the responsibilities set out in the JSE Listing Requirements paragraph 5.7(h)" `[D001, physical PDF p. 60]` — a compliance claim, not a financial disclosure; verify against the audit committee report in D002/D003.
- p. 59 board skills matrix uses "OOO Core/deep expertise" and "OO Strong experience" legend markers; the matrix cells themselves are not populated in the captured text (only the legend and director/role rows appear). This is a capture limitation, not a report omission — flag for re-capture if board skills composition is needed for governance scoring.

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| N1 | High | D002 Financial review / D003 | p. 59 lists Ivan Saltzman and Stan Goetsch as "Executive Director (Non-Executive Director post June 2026)" `[D001, p. 59]` | In D002/D003 remuneration and related-party notes, confirm whether any FY2026 amounts relate to the executive-to-NED transition, and whether FY2027 NED fees are disclosed. State amounts in Rm or confirm nil. | Affects FY2027 executive cost base and related-party disclosure. |
| N2 | Medium | D002 / D003 | p. 60 Audit and Risk Committee "has executed the responsibilities set out in the JSE Listing Requirements paragraph 5.7(h)" `[D001, p. 60]` | Locate the audit committee report and confirm the same compliance statement; check whether any internal control deficiencies or significant audit findings are disclosed. | Governance/control risk affects forecast reliability of reported numbers. |
| N3 | Medium | D002 / D003 | p. 62 "All committees have fulfilled their responsibilities as set out in the Listing Requirements and their terms of reference" `[D001, p. 62]` | Cross-check against the directors' responsibility statement and audit committee report; confirm no contrary disclosure. | Consistency of governance assertions with financial disclosures. |
| N4 | Low | D001 continuation (re-capture p. 59) | Board skills matrix cells not populated in captured text; only legend and director/role rows appear `[D001, p. 59]` | Re-capture p. 59 with full table cells to confirm which directors hold which skills (Retail and pharmacy operations; Healthcare and clinical; Finance, accounting and audit; Strategy, M&A and investments; Governance, legal and regulatory). | Governance scoring only; not a direct forecast driver. |

### 4. Updated Open Questions Ledger

```json
{"ledger_version": 1, "updates": [{"question_id": "Q-c08de916ece24aa2", "status": "partial", "answer": "p. 59 confirms Ivan Saltzman and Stan Goetsch are listed as 'Executive Director (Non-Executive Director post June 2026)'. No remuneration, share-based payment, or related-party amounts disclosed on pp. 59-62. Remainder open for D002/D003.", "evidence": [{"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 59, "quote": "Ivan Saltzman | Executive Director (Non-Executive Director post June 2026)"}, {"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 59, "quote": "Stan Goetsch | Executive Director (Non-Executive Director post June 2026)"}]}, {"question_id": "Q-c0abddef102f479a", "status": "partial", "answer": "p. 59 confirms the Saltzman executive-to-NED transition ('post June 2026'). FY2026 year-end date not stated in this capture; no transition-related remuneration/share-based/related-party amounts disclosed on pp. 59-62. Remainder open for D002/D003.", "evidence": [{"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 59, "quote": "Ivan Saltzman | Executive Director (Non-Executive Director post June 2026)"}]}, {"question_id": "Q-b0bf6b4f350046e5", "status": "partial", "answer": "p. 59 confirms Goetsch and Ivan Saltzman transitions ('post June 2026'). No transition-related remuneration/share-based/related-party amounts disclosed on pp. 59-62. Remainder open for D002/D003.", "evidence": [{"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 59, "quote": "Stan Goetsch | Executive Director (Non-Executive Director post June 2026)"}]}], "new_questions": [{"question": "In D002/D003 remuneration and related-party notes, confirm whether any FY2026 amounts relate to the Ivan Saltzman and Stan Goetsch executive-to-NED transitions (effective post June 2026), and whether FY2027 NED fees are disclosed. State amounts in Rm or confirm nil.", "priority": "high", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D002 Financial review / D003 remuneration & related-party notes", "evidence_required": "Director remuneration table, share-based payment note, and related-party note for FY2026 vs FY2025 in Rm, with page citations; explicit statement if transition-related amounts are nil.", "closure_condition": "Transition-related remuneration/share-based/related-party amounts quantified or confirmed nil, with source pages cited; impact on FY2027 cost base noted."}, {"question": "Locate the audit committee report and confirm the p. 60 statement that the Audit and Risk Committee 'has executed the responsibilities set out in the JSE Listing Requirements paragraph 5.7(h)'; check whether any internal control deficiencies or significant audit findings are disclosed.", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D002 Financial review / D003", "evidence_required": "Audit committee report text with page citation; any internal control deficiency or significant audit finding disclosures; explicit statement if none.", "closure_condition": "Audit committee compliance statement confirmed with citation; any control deficiencies/findings quantified or confirmed absent."}, {"question": "Cross-check the p. 62 statement 'All committees have fulfilled their responsibilities as set out in the Listing Requirements and their terms of reference' against the directors' responsibility statement and audit committee report; confirm no contrary disclosure.", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D002 / D003", "evidence_required": "Directors' responsibility statement and audit committee report text with page citations; explicit statement of consistency or contradiction.", "closure_condition": "Consistency confirmed with citation, or contradiction flagged with source pages."}, {"question": "Re-capture physical PDF p. 59 with full board skills matrix cells populated to confirm which directors hold which skills (Retail and pharmacy operations; Healthcare and clinical; Finance, accounting and audit; Strategy, M&A and investments; Governance, legal and regulatory).", "priority": "low", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D001 continuation (p. 59)", "evidence_required": "Full board skills matrix table with all cells populated, with page citation.", "closure_condition": "Skills matrix cells captured and director-skill mapping confirmed."}]}
```

### 5. Baseline Forecast Inputs Captured Here

| Item | Value | Source |
| --- | --- | --- |
| Board size (directors listed) | 11 | `[D001, p. 59]` |
| Executive directors | 3 (Rui Morais CEO; Julia Pope CFO; Ivan Saltzman, Stan Goetsch — both NED post June 2026) | `[D001, p. 59]` |
| Independent NEDs | 5 (Larry Nestadt chair; Anuschka Coovadia; Happy Masondo; Joe Mthimunye; Alupheli Sithebe) | `[D001, p. 59]` |
| Non-independent NEDs | 2 (Saul Saltzman; Katlego Kobue) | `[D001, p. 59]` |
| Audit and Risk Committee members | 4 (Joe Mthimunye chair; Alupheli Sithebe; Anuschka Coovadia; Happy Masondo) | `[D001, p. 60]` |
| Remuneration Committee members | 4 (Joe Mthimunye chair; Larry Nestadt; Katlego Kobue; Happy Masondo) | `[D001, p. 61]` |
| Nominations Committee members | 4 (Larry Nestadt chair; Joe Mthimunye; Katlego Kobue; Happy Masondo) | `[D001, p. 61]` |
| Social and Ethics Committee members | 3 (Alupheli Sithebe chair; Anuschka Coovadia; Happy Masondo) | `[D001, p. 62]` |

No financial figures (revenue, margin, debtor, store, lease, capex, HEPS, DPS) appear in this capture.

### 6. Next Section to Capture

**D002 Financial review (physical pp. 103–107)** — will resolve the revenue/total-income tables (Q-9dcda868ba3541df), segmental and wholesale splits (Q-f9bd0d6e26184619, Q-a0b5279a24d84ae3), category revenue (Q-418d71d0400347b3), store count reconciliation (Q-2791af76c6484354), and the remuneration/related-party transition amounts (Q-c08de916ece24aa2, Q-c0abddef102f479a, Q-b0bf6b4f350046e5, N1).
VALIDATION ERRORS:
["Evidence quote for Q-c08de916ece24aa2, physical page 59 is not literal: 'Ivan Saltzman | Executive Director (Non-Executive Director post June 2026)'. Use a short verbatim excerpt or keep this question open without claiming resolution."]