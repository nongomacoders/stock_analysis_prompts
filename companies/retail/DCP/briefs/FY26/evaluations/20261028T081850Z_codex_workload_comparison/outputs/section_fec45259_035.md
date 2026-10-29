### 1. Stored Questions Answered in This Section

No stored questions were supplied in the prompt (the stored-questions block was empty). All questions listed under “Questions Specifically for This Section" remain open and are carried forward in Section 4.

---

### 2. Footnote & Qualification Deep-Dive

- **`[^14]` — footnote marker present, definition absent.** The marker appears next to the retail segment chart on p. 104 `[D002, physical PDF p. 104]`. The corresponding footnote text is **not present in this capture**. It cannot be reconstructed. A verification question is raised (Q-new-1) to locate the definition in D003/D006.
- **"FY2025: 30.7% excluding property gain"** `[D002, physical PDF p. 105]` — the FY2025 total income margin comparator is stated on a *normalised* basis (property gain excluded). The FY2026 30.8% is therefore not directly comparable to the as-reported FY2025 margin. The property gain amount and its line placement (other income vs revenue) must be verified in D003/D006 before using the margin trend in the forecast.
- **"Employment costs, excluding the investment in X, bigly labs, increased by 10.3%"** `[D002, physical PDF p. 105]` — the 13% total opex increase includes X/bigly labs establishment costs; the underlying employment cost growth is 10.3%. The X/bigly labs cost quantum is not quantified here — must be extracted from D003/D006 to separate recurring vs one-off opex.
- **"Debtor collections remained well controlled"** `[D002, physical PDF p. 105]` — qualitative only; no satisfactory-paid %, collection rate, or ECL figures in this capture. Debtors days rose 28→30. Must be tested against the credit book disclosure (D003/D006).
- **"Margin performance in the wholesale division remained under pressure due to competitive dynamics and the timing of logistics fees earned"** `[D002, physical PDF p. 105]` — flags a timing element in wholesale margin; the logistics fee amount and timing are not quantified. Verify in segmental note.
- **"Net working capital at 24.4 days has decreased from 24.8 days on 28 February 2025"** `[D002, physical PDF p. 105]` — the table shows "Total working capital 24 / 25" (rounded), while the text gives 24.4 / 24.8. Minor rounding tension; note for reconciliation but not material.
- **"The new Dis-Chem app will launch in the 2027 financial year"** `[D002, physical PDF p. 104]` — forward-looking; no capex quantification. Flag for guidance section.

---

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section | Claim / anomaly / footnote trigger | Specific verification instruction | Why it matters for forecast |
| --- | --- | --- | --- | --- | --- |
| Q-new-1 | High | D003 / D006 | Footnote `[^14]` marker on p. 104 retail segment chart; definition not printed in capture `[D002, p. 104]` | Locate verbatim `[^14]` text; state which table/category it qualifies and any figure it changes | Unknown qualification could alter retail revenue/margin read |
| Q-new-2 | High | D003 / D006 | FY2025 total income margin "30.7% excluding property gain" `[D002, p. 105]` | Extract property gain amount, its line (other income/revenue), and as-reported FY2025 total income margin | Margin trend comparability; normalised vs reported base for forecast |
| Q-new-3 | High | D003 / D006 | Opex +13% to R11.4bn incl. X/bigly labs; employment costs ex-X +10.3% `[D002, p. 105]` | Quantify X/bigly labs establishment + operating costs FY2026 vs FY2025; confirm recurring vs one-off | Separates structural opex step-up from one-offs for margin forecast |
| Q-new-4 | High | D003 / D006 | Debtors days 28→30; "collections well controlled" qualitative only `[D002, p. 105]` | Extract gross debtors, ECL allowance, debtor cost %, satisfactory-paid %, collection rate, write-offs FY2026 vs FY2025 | Credit book health drives impairment charge and cash conversion |
| Q-new-5 | Medium | D003 segmental note | Wholesale revenue +13.1% to R34bn; margin "under pressure…timing of logistics fees" `[D002, p. 105]` | Extract wholesale external vs intergroup revenue, gross margin %, logistics fee amount/timing, both years | Wholesale margin trajectory and intergroup elimination |
| Q-new-6 | Medium | D003 / D006 | Retail revenue +9.0% to R36.6bn; comparable store sales +5.3%; net 31 pharmacy stores, 3 Baby City closures `[D002, p. 104]` | Confirm retail revenue Rm both years, comp sales basis, store count reconciliation (285+33−2=316; 45−3=42) | Store rollout vs comp growth split for revenue build |
| Q-new-7 | Medium | D003 / D006 | Cash generated from operations R1.8bn (FY2025 R0.9bn); cash flow waterfall figures on p. 105 (3 124, (530), (402), (524), (1 089), (139), 767, (995), 429) `[D002, p. 105]` | Map each waterfall bar to cash flow statement line; confirm units (R’000 vs Rm) and reconciliation to net decrease in cash | Cash conversion and dividend/capex funding capacity |
| Q-new-8 | Low | D003 / D006 | Inventory days 86 (FY2025 91); creditors days 92 (94) `[D002, p. 105]` | Confirm inventory and creditor balances and day-count basis (cost of sales vs revenue denominator) | Working capital forecast inputs |

---

### 4. Updated Open Questions Ledger

```json
{"ledger_version": 1, "updates": [], "new_questions": [
{"question": "Locate and state verbatim the definition of footnote [^14] that appears next to the retail segment chart on physical p. 104; identify which table/category it qualifies and whether it changes any retail revenue or margin figure for FY2026 vs FY2025.", "priority": "high", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D003 / D006", "evidence_required": "Verbatim [^14] text with page citation; the table/category it attaches to; any figures it qualifies, both years, Rm/%.", "closure_condition": "Footnote [^14] text reproduced verbatim with page citation, or explicit statement it is not printed anywhere in the report; any affected retail revenue/margin figure identified."},
{"question": "Extract the property gain excluded from the FY2025 total income margin comparator (stated 30.7% excluding property gain) and the as-reported FY2025 total income margin; state the line item (other income vs revenue) and amount.", "priority": "high", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D003 / D006", "evidence_required": "Property gain amount Rm, line placement, as-reported FY2025 total income margin %, with page citations.", "closure_condition": "Property gain quantified and located; as-reported vs normalised FY2025 margin reconciled to FY2026 30.8%; forecast base stated."},
{"question": "Quantify the X / bigly labs establishment and operating costs included in FY2026 operating expenses (opex +13% to R11.4bn; employment costs ex-X +10.3%), and confirm which components are recurring vs one-off.", "priority": "high", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D003 / D006", "evidence_required": "X/bigly labs cost amounts Rm, split by nature (employment, other), FY2026 vs FY2025, with page citations; recurring vs one-off classification.", "closure_condition": "X/bigly labs costs quantified and classified; opex growth reconciled to 13% total and 10.3% ex-X employment growth."},
{"question": "Extract the credit/debtors book metrics for FY2026 vs FY2025: gross carrying debtors, ECL impairment allowance, debtor cost as % of gross debtors, satisfactory-paid customer %, collection rate %, and write-offs, to test the 'debtor collections remained well controlled' claim alongside debtors days rising 28→30.", "priority": "high", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D003 / D006", "evidence_required": "Debtors book table: gross debtors, ECL allowance, debtor cost %, satisfactory-paid %, collection rate %, write-offs, both years, Rm/%, with page citations.", "closure_condition": "All credit metrics extracted for both years; debtors days 28→30 reconciled to balances; impairment charge consistent with ECL movement."},
{"question": "Extract wholesale segment external vs intergroup revenue and gross margin for FY2026 vs FY2025 (revenue +13.1% to R34bn), and quantify the 'timing of logistics fees earned' referenced as a margin pressure factor.", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D003 segmental note", "evidence_required": "Wholesale revenue split external vs intergroup, gross margin %, logistics fee amount/timing, both years, Rm, with page citations.", "closure_condition": "External vs intergroup wholesale revenue and margin extracted for both years; logistics fee timing quantified; intergroup elimination consistent with group revenue."},
{"question": "Confirm retail revenue R36.6bn (+9.0%), comparable store sales +5.3% basis, and reconcile store counts: 285+33−2=316 pharmacy stores and 45−3=42 Baby City stores, with net 31 pharmacy openings and 3 Baby City closures.", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D003 / D006", "evidence_required": "Retail revenue Rm both years; comp sales definition; store count roll-forward by brand, with page citations.", "closure_condition": "Retail revenue and comp sales basis confirmed; store counts reconcile to 316 and 42; revenue growth split between comp and new stores."},
{"question": "Map the cash flow waterfall figures on p. 105 (3 124, (530), (402), (524), (1 089), (139), 767, (995), 429) to the cash flow statement lines, confirm units (R’000 vs Rm), and reconcile to net decrease in cash and cash generated from operations of R1.8bn (FY2025 R0.9bn).", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D003", "evidence_required": "Cash flow statement lines matching each waterfall bar, units stated, reconciliation to net cash movement, with page citations.", "closure_condition": "Each waterfall bar mapped to a cash flow line; units confirmed; total reconciles to net decrease in cash; R1.8bn operating cash confirmed."},
{"question": "Confirm inventory days 86 (FY2025 91) and creditors days 92 (FY2025 94) day-count basis (denominator: cost of sales vs revenue) and the underlying inventory and creditor balances.", "priority": "low", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D003 / D006", "evidence_required": "Inventory and trade creditor balances Rm both years; day-count formula/denominator stated; page citations.", "closure_condition": "Day-count basis confirmed; balances extracted; days recomputed and reconciled to 86/91 and 92/94."}
]}
```

---

### 5. Baseline Forecast Inputs Captured Here

| Metric | FY2026 | FY2025 | Source |
| --- | --- | --- | --- |
| Retail revenue | R36.6bn (+9.0%) | — | D002 p.104 |
| Comparable store sales growth | +5.3% | — | D002 p.104 |
| Wholesale revenue | R34bn (+13.1%) | — | D002 p.105 |
| Total income margin | 30.8% | 30.7% (excl. property gain) | D002 p.105 |
| Operating expenses | R11.4bn (+13%) | — | D002 p.105 |
| Employment costs ex-X/bigly labs growth | +10.3% | — | D002 p.105 |
| Cash generated from operations | R1.8bn | R0.9bn | D002 p.105 |
| Debtors days | 30 | 28 | D002 p.105 |
| Inventory days | 86 | 91 | D002 p.105 |
| Creditors days | 92 | 94 | D002 p.105 |
| Net working capital days | 24.4 | 24.8 | D002 p.105 |
| Pharmacy stores (year-end) | 316 | 285 | D002 p.104 |
| Baby City stores (year-end) | 42 | 45 | D002 p.104 |
| Net pharmacy store openings | 31 | — | D002 p.104 |
| Baby City closures | 3 | — | D002 p.104 |
| New app launch | FY2027 | — | D002 p.104 |

---

### 6. Next Section to Capture

**D003 (Primary financial statements, pp. 108–123)** — resolves Q-new-2 (property gain), Q-new-3 (X/bigly labs costs), Q-new-4 (debtors book), Q-new-5 (wholesale split), Q-new-6 (retail revenue/store reconciliation), Q-new-7 (cash flow mapping), Q-new-8 (inventory/creditor balances). Q-new-1 (`[^14]`) may require D006 notes if not defined in D003.