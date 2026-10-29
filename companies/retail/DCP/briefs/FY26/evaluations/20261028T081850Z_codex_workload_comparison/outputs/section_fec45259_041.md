### 1. Stored Questions Answered by This Section

- **Q-d02fca7998ed4334** — *Status: Partially resolved (FY2026 period end and results date confirmed; FY2025 comparative period end still open)*
  - FY2026 year-end confirmed as 28 February 2026 ("Full-year results to 28 February 2026", "Interim results to 31 August 2026") `[D004, physical PDF p. 128]`. Results publication date confirmed as Friday, 29 May 2026 `[D004, physical PDF p. 128]`. FY2025 comparative period end not stated in this capture — remains open for D003/D006.

- **Q-e9df7e72a7c4457d** — *Status: Partially resolved (Better Rewards abbreviation confirmed; launch date, cohort basis and liability still open)*
  - "BR = Better Rewards" confirmed in abbreviations `[D004, physical PDF p. 129]`. No launch date, 17-week cohort basis, or rewards liability/provision appears in this capture — remains open for D003/D006.

- **Q-29036196fb1a4436** — *Status: Partially resolved (final dividend timetable confirmed; DPS amounts and payout policy still open)*
  - FY2026 final dividend timetable confirmed: LDT cum-dividend Mon 15 June 2026; ex-dividend Wed 17 June 2026; record Fri 19 June 2026; payment Mon 22 June 2026 `[D004, physical PDF p. 128]`. DPS amounts, interim DPS, FY2025 total DPS and payout policy target not in this capture — remain open for D006 dividends note / D002.

- **Q-1a634a1ef73f4bf4** — *Status: Partially resolved (IAR/SR publication date confirmed; subsequent-events window still open)*
  - "Publication of IAR and SR — Tuesday, 30 June 2026" confirms the 30 June 2026 IAR approval/publication date referenced in the question `[D004, physical PDF p. 128]`. Subsequent-events note and window not in this capture — remains open for D006.

- **Q-54415b5d341747e7** — *Status: Partially resolved (LTI/STI abbreviations confirmed; remuneration report population and expense still open)*
  - "LTI = Long-term incentive", "STI = Short-term incentive", "WANOS = Weighted average number of shares", "TCoE = Total Cost of Employment", "TGP = Total Guaranteed Package" confirmed in abbreviations `[D004, physical PDF p. 129]`. No remuneration implementation report content or share-based payment expense in this capture — remains open for D002/D006.

- **Q-a9bb4b924fdd4bfc / Q-e9ec431611354b52** — *Status: Partially resolved (definitions only; expense and share movements still open)*
  - HEPS defined as "Headline earnings / WANOS"; EPS as "Earnings attributable to equity holders / WANOS" `[D004, physical PDF p. 130]`. No expense figures or share movements — remain open for D006 share-based payment note.

- **Q-2791af76c6484354 / Q-66ba1f0e71b74f99 / Q-a7aa879cbd064579 / Q-cbbfe2e5a90d4260 / Q-d1f917e510ff41f3** — *Status: Not addressed by this capture; carried forward unchanged.*

### 2. Footnote & Qualification Deep-Dive

- **No footnote markers (`[^1]`, `*`) present** in any of the supplied pages (128–132). No missing-footnote issue to flag.
- **Shareholders' diary anomaly** `[D004, physical PDF p. 128]`: "Full-year results to 28 February 2027 — Friday, 28 May 2026". This is internally inconsistent — a FY2027 results date cannot precede the FY2027 year-end (28 Feb 2027). Likely a typo for 28 May 2027. Flagged as verification question (see Q#1 below); matters for forecast calendar alignment only, not for FY2026 numbers.
- **Definitional qualifications** `[D004, physical PDF p. 130]`:
  - **Debtors Days** formula uses *Revenue* (not credit sales) as denominator: `(Average trade and other receivables) / Revenue × 365`. This understates true credit-collection days because cash sales inflate the denominator. Any debtor-days figure quoted elsewhere in the report must be checked against this definition before use in the forecast.
  - **Creditors Days** formula uses `(Cost of goods sold + trade terms)` — the "+ trade terms" add-back is unusual and not defined; needs verification against the actual computation in D002/D006.
  - **Dividend Payout Ratio** defined as `Dividends paid / Net income` — note this is *dividends paid* (cash), not *declared DPS*, so it may differ from a DPS/EPS calculation. Relevant to Q-29036196fb1a4436.
  - **Like-for-like Revenue Growth** defined as stores open "at least two full financial years" — confirms the LFL cohort basis for forecast modelling.
  - **Net Working Capital Days** = Debtor days + Inventory days − Creditor days — confirms the NWC bridge definition.
  - **ROCE** = EBIT / Capital employed; **ROE** = Net income attributable to equity holders / Average shareholders' equity — confirms return metric definitions.
- **Corporate information** `[D005, physical PDF p. 131]`: JSE code DCP, ISIN ZAE000227831, registration 2005/009766/06; auditors Forvis Mazars; sponsor Standard Bank; transfer secretaries JSE Investor Services. No financial figures.
- **D006 p. 132**: only "dischemgroup.com" extracted — sparse page, no usable content; requires source inspection.

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section | Claim / anomaly / footnote trigger `[D00X, p. Y]` | Specific verification instruction | Why it matters for forecast |
| --- | --- | --- | --- | --- | --- |
| 1 | Medium | D004 (re-check) / D002 | "Full-year results to 28 February 2027 — Friday, 28 May 2026" `[D004, p. 128]` — date precedes year-end | Confirm correct FY2027 results date (likely 28 May 2027); check any SENS/provisional-report calendar | Calendar alignment for forecast period roll-forward |
| 2 | High | D002 / D006 | Debtors Days defined using Revenue (incl. cash sales) as denominator `[D004, p. 130]` | Locate actual Debtors Days figure in D002/D006 and confirm denominator used; reconcile to gross debtors and credit sales mix | Credit-book cash absorption and working-capital forecast |
| 3 | Medium | D002 / D006 | Creditors Days formula includes undefined "+ trade terms" `[D004, p. 130]` | Confirm actual Creditors Days computation and whether trade terms add-back is applied | NWC days and supplier-financing forecast |
| 4 | Medium | D006 (dividends note) | Payout ratio defined as Dividends paid / Net income (cash basis) `[D004, p. 130]` | Reconcile stated payout ratio to DPS/EPS and to cash dividends paid; confirm policy target basis | Dividend forecast and payout sustainability |
| 5 | Low | D006 | D006 p. 132 sparse — only "dischemgroup.com" extracted `[D006, p. 132]` | Inspect source page 132 for any financial content (likely back cover); confirm no material disclosure | Completeness of report capture |

### 4. Updated Open Questions Ledger

```json
{"ledger_version": 1, "updates": [{"question_id": "Q-d02fca7998ed4334", "status": "partial", "answer": "FY2026 year-end confirmed as 28 February 2026 and full-year results publication date confirmed as Friday 29 May 2026. FY2025 comparative period end not stated in this capture.", "evidence": [{"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 128, "quote": "Full-year results to 28 February 2026"}, {"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 128, "quote": "Friday, 29 May 2026"}]}, {"question_id": "Q-e9df7e72a7c4457d", "status": "partial", "answer": "Better Rewards abbreviation (BR) confirmed. Launch date, 17-week cohort basis and any rewards liability/provision not present in this capture.", "evidence": [{"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 129, "quote": "BR     Better Rewards"}]}, {"question_id": "Q-29036196fb1a4436", "status": "partial", "answer": "FY2026 final dividend timetable confirmed (LDT 15 June 2026, ex-div 17 June 2026, record 19 June 2026, payment 22 June 2026). DPS amounts, interim DPS, FY2025 total DPS and payout policy target not in this capture.", "evidence": [{"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 128, "quote": "Payment date: FY2026 final dividend"}, {"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 128, "quote": "Monday, 22 June 2026"}]}, {"question_id": "Q-1a634a1ef73f4bf4", "status": "partial", "answer": "IAR and SR publication date confirmed as Tuesday 30 June 2026. Subsequent-events note and window not in this capture.", "evidence": [{"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 128, "quote": "Publication of IAR and SR"}, {"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 128, "quote": "Tuesday, 30 June 2026"}]}, {"question_id": "Q-54415b5d341747e7", "status": "partial", "answer": "LTI/STI/WANOS/TCoE/TGP abbreviations confirmed. Remuneration implementation report population and share-based payment expense not in this capture.", "evidence": [{"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 129, "quote": "LTI    Long-term incentive"}, {"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 129, "quote": "STI    Short-term incentive"}]}, {"question_id": "Q-a9bb4b924fdd4bfc", "status": "partial", "answer": "HEPS and EPS definitions confirmed (Headline earnings / WANOS; Earnings attributable to equity holders / WANOS). Expense and share movements not in this capture.", "evidence": [{"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 130, "quote": "Headline earnings / WANOS"}]}, {"question_id": "Q-e9ec431611354b52", "status": "partial", "answer": "Definitions only confirmed in this capture; LTI/FSP terms and share-based payment expense not present.", "evidence": [{"source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6", "physical_page": 130, "quote": "Headline earnings / WANOS"}]}], "new_questions": [{"question": "Confirm the correct FY2027 full-year results publication date, given the shareholders' diary states 'Full-year results to 28 February 2027 — Friday, 28 May 2026', which precedes the FY2027 year-end.", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D004 (re-check) / D002", "evidence_required": "Corrected FY2027 results date with page citation; any SENS or provisional-report calendar reference.", "closure_condition": "Correct FY2027 results date confirmed with citation, or typo confirmed and corrected date stated."}, {"question": "Confirm the actual Debtors Days figure reported in the financial review and whether the denominator is Revenue (including cash sales) as per the p.130 definition, reconciling to gross debtors and the credit/cash sales mix.", "priority": "high", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D002 Financial review / D006 Notes", "evidence_required": "Reported Debtors Days figure, denominator used, gross debtors (Rm), credit vs cash sales split, with page citations.", "closure_condition": "Debtors Days figure and denominator confirmed; reconciliation to gross debtors and sales mix shown, or discrepancy quantified."}, {"question": "Confirm the actual Creditors Days computation and whether the undefined '+ trade terms' add-back in the p.130 formula is applied in the reported figure.", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D002 Financial review / D006 Notes", "evidence_required": "Reported Creditors Days figure, computation basis, trade payables (Rm), COGS (Rm), with page citations.", "closure_condition": "Creditors Days computation confirmed with citation; trade-terms add-back treatment stated."}, {"question": "Reconcile the stated Dividend Payout Ratio (defined as Dividends paid / Net income) to DPS/EPS and to cash dividends paid, and confirm the policy target basis.", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D006 dividends note / D002 dividend policy", "evidence_required": "Stated payout ratio, DPS, EPS/HEPS, cash dividends paid (Rm), policy target %, with page citations.", "closure_condition": "Payout ratio reconciled on both bases; policy target basis confirmed with citation."}, {"question": "Inspect source page 132 for any financial content beyond 'dischemgroup.com' and confirm no material disclosure is omitted from the capture.", "priority": "low", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D006", "evidence_required": "Full text of physical page 132; explicit statement if back cover only.", "closure_condition": "Page 132 content confirmed as non-financial or any financial content extracted with citation."}]}
```

### 5. Baseline Forecast Inputs Captured Here

| Item | Value | Source |
| --- | --- | --- |
| FY2026 year-end | 28 February 2026 | `[D004, p. 128]` |
| FY2026 full-year results date | 29 May 2026 | `[D004, p. 128]` |
| IAR/SR publication | 30 June 2026 | `[D004, p. 128]` |
| FY2026 interim period end | 31 August 2026 | `[D004, p. 128]` |
| FY2026 final dividend — LDT cum | 15 June 2026 | `[D004, p. 128]` |
| FY2026 final dividend — ex-div | 17 June 2026 | `[D004, p. 128]` |
| FY2026 final dividend — record | 19 June 2026 | `[D004, p. 128]` |
| FY2026 final dividend — payment | 22 June 2026 | `[D004, p. 128]` |
| AGM date | 31 July 2026, 10am | `[D004, p. 128]` |
| JSE code / ISIN | DCP / ZAE000227831 | `[D005, p. 131]` |
| Auditors | Forvis Mazars | `[D005, p. 131]` |
| Sponsor | Standard Bank of South Africa | `[D005, p. 131]` |
| LFL definition | Stores open ≥ 2 full financial years | `[D004, p. 130]` |
| NWC days definition | Debtor days + Inventory days − Creditor days | `[D004, p. 130]` |

### 6. Next Section to Capture

**D002 Financial review (pp. 103–107)** — resolves Q#2 (Debtors Days), Q#3 (Creditors Days), Q-29036196fb1a4436 (DPS/payout), Q-54415b5d341747e7 (remuneration expense), and Q-cbbfe2e5a90d4260 (IT/cyber costs). D003 primary statements (pp. 108–123) and D006 notes (p. 132) remain the priority follow-ups for share-based payment, Ivlyn restructure, and subsequent-events items.