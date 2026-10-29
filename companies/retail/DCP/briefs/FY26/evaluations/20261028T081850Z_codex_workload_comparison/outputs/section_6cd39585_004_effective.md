### 1. Answers to Stored Questions for This Section

No stored questions can be resolved from this single page. The evidence on physical p. 6 is a revenue and total-income table with CID-encoded glyphs; it does not contain the auditor's report, cash flow statement, notes, credit book metrics, store portfolio, or subsequent events required by the stored ledger. All stored questions are carried forward unchanged in Section 4.

One stored question is **partially advanced**:

- **Question ID**: `Q-be16064fca7945fd`
- **Status**: `Partially resolved (remainder stays open for D001 continuation pp. 7-24 / D002)`
- **Answer & evidence**: Physical p. 6 supplies the revenue and total-income lines only. Decoded from the glyph pattern: Revenue FY2026 R41,596m vs FY2025 R37,954m (+9.6%); Store sales R40,488m vs R30,033m (+12.1%); Intergroup R(1,814)m vs R(1,891)m (+12.9%); Total group R42,826m vs R39,156m (+9.3%); Total income R11,190m vs R10,159m (+12.6%); Store sales total income R2,699m vs R2,599m (-8.1%); Intergroup R(739)m vs R(566)m (+12.3%); Total income R13,216m vs R12,182m (+8.5%); Total income margin 30.9% vs 31.0% (30.7% excluding property gain). These are **decoded, not verified** — the CID encoding means exact digits must be confirmed against a plain-text capture. Merchandise vs customer financial services split, gross margin %, debtor cost %, satisfactory-paid %, collection rate %, store count, trading space m², HEPS, DPS, capex and net debt are **not** on this page and remain open for pp. 7-24 / D002.

### 2. Footnote & Qualification Deep-Dive

- **No footnote markers (`[^1]`, `*`, note references) are present on physical p. 6.** There is therefore no footnote text to unpack or to flag as missing from this capture. This is itself a verification point: the revenue and total-income tables carry no printed qualifications, so any adjustment (property gain, ecosystem expenses, intergroup elimination basis) must be sought on adjacent pages (p. 5 and pp. 7-24).
- **Embedded qualification — "excluding property gain"**: The total-income table presents a second "% change" and "% margin" column explicitly *excluding property gain* (FY2026 30.7% vs FY2025 30.7%). This is a management-adjusted basis, not a statutory one. It implies a property gain is embedded in FY2026 total income (and possibly FY2025) that management considers non-recurring. The rand amount of that gain is **not printed on this page** — it must be quantified on p. 5 or in the notes (Note 8 / PPE disposal note). Until quantified, the 30.9% headline margin overstates the recurring margin by an unknown amount.
- **Embedded qualification — "excluding the property gain" in the store-sales total-income bullet**: The bullet states store-sales total income declined 8.1% *including* the property gain but rose 0% *excluding* it (R2,699m vs R2,696m). This is a material qualification: the headline -8.1% is flattered/distorted by a property gain sitting in the prior or current year base. The exact gain amount and which year it falls in must be verified.
- **Intergroup elimination basis**: Intergroup revenue R(1,814)m and intergroup total income R(739)m are shown as separate elimination lines. The intergroup total-income elimination (R739m) is large relative to total income (R13,216m) — ~5.6% — and its growth (+12.3%) outpaces group revenue growth (+9.3%). The basis of intergroup margin (i.e., whether intergroup sales carry a different margin than external sales) is not explained here and should be checked in the segmental note.
- **"Total income" vs "revenue" definition**: The page uses "total income" (R13,216m) which is larger than "total group revenue" (R42,826m) only as a margin concept — total income margin 30.9%. The composition of total income (gross profit + other income + customer financial services revenue?) is not defined on this page and must be confirmed against the income statement (D002) and Note 7.

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D001, p. 6]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| N1 | High | D002 (physical pp. 30-39) / D005 Note 8 | Total-income table shows a separate "excluding property gain" column (30.7% vs 30.7%) implying an unquantified property gain in FY2026 and/or FY2025 `[D001, p. 6]` | Locate the property gain rand amount FY2026 vs FY2025 in the income statement, Note 8 (other income) or PPE/disposal note; confirm which year it falls in and whether non-recurring | Determines the recurring total-income margin base for FY2027; if the gain is in FY2026, the 30.9% headline overstates the run-rate |
| N2 | High | D002 / D005 Note 7 | "Total income" R13,216m (margin 30.9%) is used but not defined on p. 6; revenue R42,826m and total income R13,216m imply a 30.9% margin `[D001, p. 6]` | Confirm the composition of "total income" (gross profit + other income + customer financial services revenue?) and reconcile R13,216m to the income statement and Note 7 disaggregation | Defines the margin driver for the forecast; mis-definition would distort gross margin vs total income margin |
| N3 | High | D002 / D005 Note 7 | Store-sales total income fell 8.1% including property gain but 0% excluding it (R2,699m vs R2,696m) `[D001, p. 6]` | Verify the store-sales total-income figures and the property-gain adjustment; confirm whether the gain sits in FY2025 or FY2026 base | Tests whether store-level profitability is genuinely flat or declining; drives FY2027 store margin forecast |
| N4 | Medium | D002 / D005 segmental note | Intergroup total-income elimination R739m (+12.3%) grows faster than group revenue (+9.3%) and is ~5.6% of total income `[D001, p. 6]` | Confirm intergroup margin basis and elimination in the segmental note; check whether intergroup sales carry a different margin than external sales | Affects consolidated margin and segmental profitability forecast |
| N5 | Medium | D002 (physical pp. 30-39) | Revenue decoded as R41,596m (FY2026) vs R37,954m (FY2025) and total group R42,826m vs R39,156m, but all figures are CID-encoded `[D001, p. 6]` | Re-capture p. 6 in plain text and confirm each decoded figure verbatim against the income statement | Baseline revenue and total-income figures for the forecast model must be exact |
| N6 | Low | D001 continuation (pp. 7-24) | No footnote markers on p. 6 despite management-adjusted "excluding property gain" columns `[D001, p. 6]` | Check whether the property-gain adjustment is footnoted on p. 5 or pp. 7-24; if not, flag as an unqualified management adjustment | Governance/transparency check on adjusted metrics used in guidance |

### 4. Updated Open Questions Ledger
```json
{
  "ledger_version": 1,
  "updates": [],
  "new_questions": [
    {
      "question": "What is the rand amount and year of the property gain embedded in total income, given the p. 6 total-income table presents a separate 'excluding property gain' column (30.7% vs 30.7%)?",
      "priority": "high",
      "target_document": "1780031786-FY2026AnalystPresentation.pdf",
      "target_section": "D002 (physical pp. 30-39) / D005 Note 8",
      "evidence_required": "Property gain rand amount FY2026 vs FY2025 from income statement, Note 8 (other income) or PPE/disposal note; confirmation of which year it falls in and whether non-recurring.",
      "closure_condition": "Gain quantified for both years, year of recognition confirmed, and non-recurrence assessed; recurring total-income margin base for FY2027 stated."
    },
    {
      "question": "What is the composition of 'total income' R13,216m (margin 30.9%) used on p. 6, and does it reconcile to gross profit plus other income plus customer financial services revenue in the income statement and Note 7?",
      "priority": "high",
      "target_document": "1780031786-FY2026AnalystPresentation.pdf",
      "target_section": "D002 / D005 Note 7",
      "evidence_required": "Definition and composition of total income; reconciliation of R13,216m to income statement lines and Note 7 disaggregation, FY2026 vs FY2025.",
      "closure_condition": "Composition stated and reconciled to the income statement and Note 7; any definitional difference from gross margin explained."
    },
    {
      "question": "Do the store-sales total-income figures (R2,699m FY2026 vs R2,599m FY2025, -8.1% including property gain but 0% excluding it) reconcile to the segmental note, and is the property gain in the FY2025 or FY2026 base?",
      "priority": "high",
      "target_document": "1780031786-FY2026AnalystPresentation.pdf",
      "target_section": "D002 / D005 segmental note",
      "evidence_required": "Store-sales total-income figures FY2026 vs FY2025; property-gain adjustment; reconciliation to segmental note.",
      "closure_condition": "Figures reconciled and property-gain year confirmed; store-level margin trend for FY2027 stated."
    },
    {
      "question": "What is the intergroup margin basis behind intergroup total-income elimination of R739m (+12.3%) vs intergroup revenue elimination of R1,814m, and why does it grow faster than group revenue (+9.3%)?",
      "priority": "medium",
      "target_document": "1780031786-FY2026AnalystPresentation.pdf",
      "target_section": "D002 / D005 segmental note",
      "evidence_required": "Intergroup margin basis and elimination reconciliation in the segmental note, FY2026 vs FY2025.",
      "closure_condition": "Intergroup margin basis confirmed and elimination reconciled; impact on consolidated margin stated."
    },
    {
      "priority": "high",
      "question": "Re-capture physical p. 6 in plain text and confirm each decoded figure verbatim (Revenue R41,596m, Store sales R40,488m, Intergroup R(1,814)m, Total group R42,826m, Total income R11,190m, Store sales total income R2,699m, Intergroup R(739)m, Total income R13,216m, margins 30.9%/31.0%/30.7%), FY2026 vs FY2025, in R'm.",
      "target_document": "1780031786-FY2026AnalystPresentation.pdf",
      "target_section": "D001 continuation (pp. 7-24) / D002",
      "evidence_required": "Plain-text transcription of the p. 6 revenue and total-income tables, all line items, both years, units R'm.",
      "closure_condition": "Each decoded figure confirmed or corrected against plain text; any discrepancy stated; benign encoding explanation allowed."
    },
    {
      "question": "Is the 'excluding property gain' adjustment on p. 6 footnoted anywhere on p. 5 or pp. 7-24, and if not, is it an unqualified management adjustment?",
      "priority": "low",
      "target_document": "1780031786-FY2026AnalystPresentation.pdf",
      "target_section": "D001 continuation (pp. 7-24)",
      "evidence_required": "Footnote or qualification for the property-gain adjustment on p. 5 or pp. 7-24; if absent, explicit statement of absence.",
      "closure_condition": "Footnote located or absence confirmed; governance/transparency assessment of adjusted metric stated."
    }
  ]
}

```

### 5. Baseline Forecast Inputs Captured Here

All figures decoded from CID-encoded glyphs on `[D001, physical p. 6]` — **unverified, confirm against plain text**.

| Metric (R'm unless stated) | FY2026 | FY2025 | % change |
| --- | --- | --- | --- |
| Revenue | 41,596 | 37,954 | +9.6 |
| Store sales | 40,488 | 30,033 | +12.1 |
| Intergroup | (1,814) | (1,891) | +12.9 |
| Total group revenue | 42,826 | 39,156 | +9.3 |
| Total income (revenue line) | 11,190 | 10,159 | +12.6 |
| Store sales total income | 2,699 | 2,599 | -8.1 |
| Intergroup total income | (739) | (566) | +12.3 |
| Total income | 13,216 | 12,182 | +8.5 |
| Total income margin % | 30.9 | 31.0 | — |
| Total income margin % excl. property gain | 30.7 | 30.7 | — |

Not disclosed on this page (open for pp. 7-24 / D002): merchandise vs customer financial services split, gross margin %, debtor cost %, satisfactory-paid %, collection rate %, store count, trading space m², HEPS, DPS, capex, net debt.

### 6. Next Section to Capture

**D001 continuation, physical p. 7** (or the next available page in the pp. 7-24 commentary block). It should resolve or advance `Q-be16064fca7945fd` (remaining metrics), `Q-16620b53dedf4158` (credit book / store portfolio), `Q-8ee35ca22aec4c31` (p. 4 trading space), `Q-ed005c11cf574cc8` (store count / total income margin), and the new N1-N3 questions on the property gain and total-income composition. If p. 7 is not available, capture **D002 (physical pp. 30-39)** to obtain the primary statements needed for N1-N5.