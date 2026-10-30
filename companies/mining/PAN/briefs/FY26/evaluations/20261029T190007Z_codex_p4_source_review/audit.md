# Codex source-evidence review — PAN FY26

**Decision: corrections required.** The five targeted remediations are correct within the checks below; extraction coverage is still overstated. Reviewed 29 October 2026, Africa/Johannesburg. Source SHA-256 verified as `62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd`; 54 physical pages. The current database contains **4,802**, not 4,800 cells. Database and original reviewer output were not edited.

## 1. Verdict on the five remediations

| Claim | Verdict | Independent evidence |
|---|---|---|
| C001 — document lineage normalized | Correct | `SELECT document,COUNT(*) FROM cells GROUP BY 1` returns one row: the verified source SHA, 4,802 cells. The stated 4,800 denominator is stale after the two restored cells. |
| C002 — two Note 18 rows recovered | Correct, narrowly | Physical p.34 visibly prints ordinary shares to be issued, note **14**, **148,218**, and PPE, note **7**, **142,436**, US$ thousand. Stored IDs **10879/10880**, `note_p34`, col0, match labels, references and numbers. This does not recover the complete acquisition tables (F004). |
| C003 — headline constants asserted | Correct | p.18 EPS **17.60/7.16 US cents**, total comprehensive income **400,965/155,554 US$ thousand**; p.46 levered FCF **201.8 US$m**; p.44 net cash **(185.7)** and net senior cash **(194.7) US$m**; p.21 revenues **352,807 / 441,978 / dash / 228,268 / 132,804 / 1,155,857 / blank / 594 / blank / blank / 1,156,451** match the stored values and new assertions. The prompt's page list omits p.44 for debt; p.22 is the asset/EBITDA continuation. `test_review_fixes.py` was inspected and executed. |
| C004 — all eight questions open | Correct | All eight `questions.status` values are `open`; the eight IDs and statuses agree with consolidated brief section 5. No closure inferred from an arithmetic tie. |
| C005 — Note 17.1 roll-forward | Correct | p.33 prints positive FX **2,331/438**. FY26: **21,486 + 57,272 + 1,463 − 18,200 + 2,331 = 64,352**. FY25: **10,965 + 13,358 + 6,325 − 9,600 + 438 = 21,486**. Stored IDs 9848–9859 preserve the signs; the new test sums the movement rows in the correct direction. |

Suite rerun: **127 passed in 0.33s, exit 0**, using the main checkout's venv specified in the review prompt. This confirms execution, not complete extraction or financial validation. The brief's 109-test statement is stale.

## 2. Pass B findings

Each item identifies the printed glyph and the stored cell or its absence. Amounts below are US$ thousand unless stated otherwise.

- **F001 — p.24; severity: wrong / missing / mislabelled.** The separate **Geographical information** table prints South Africa **911,962 / 740,819**, Australia **365,207 / 155,716**, Other countries **480 / 445**, total **1,277,649 / 896,980** (FY26/FY25). IDs **3216–3218** store only the three FY25 leaves under `note3_segment_analysis`, `column_index=2`, **`column_label='Solar projects'`**; ID3216 also absorbs the preceding footnotes into its row label. All four FY26 cells and the FY25 total are absent. This is an undeclared change of table semantics on a page claimed as covered, not the declared intra-group exclusion. Isolate this two-year table and reconcile each year's three leaves to its total.
- **F002 — p.29, Note 8; severity: missing / mislabelled.** The capex table prints **21,832 + 202,163 = 223,995** and **11,626 + 156,283 = 167,909**. None of these six totals exists on p.29 in `cells`; neither do Barberton's FY26 **12,639 / 27,442 / 40,081**. Only **18 of 54** printed amount positions in Note 8 survive as numeric/dash cells; e.g. IDs **9558/9559** retain MTR FY25 **51,938/52,206**, with sustaining **268** swallowed into `row_label='FY25 268'`. The region's 68-cell total includes Notes 9–11 and is not proof that Note 8 was extracted. The absence of suite checks is declared honestly; the implied presence of its rows is not. Execute row identities and category totals after restoring the full three-column table.
- **F003 — p.35, Note 19; severity: missing.** The working-capital row **“(Increase)/decrease in other receivables” (21,206) / 2,833** is absent between IDs **9914/9915** (inventory) and **9916/9917** (payables). Thus **17,411 − 21,206 + 50,354 = 46,559** cannot be rebuilt from stored leaves. The label “printed, unverified” conceals incomplete extraction. No suite identity addresses this region. Restore the row and test adjustments, working capital and the final subtotal in both years.
- **F004 — p.34, Note 18; severity: missing; source-availability assertion wrong.** Both the rendered page and native text print **11,879** directly attributable transaction costs and **160,097** total acquisition cost / total net assets acquired. Both are absent from `note_p34`; so are **142,244, 112, 80, 86, 6,427, 12,796, (133), (1,515)** in their acquisition-allocation roles. Stored IDs **10879/10880** cover just the two note-referenced rows. The prompt's assertion that 11,879 and 160,097 are unavailable in the text layer is contradicted by a fresh extraction. Both acquisition bridges reconcile exactly when all printed rows are used.
- **F005 — p.36, Note 20.2; severity: missing / mislabelled.** The fair-value hierarchy prints FY26 Investment Level 1 **12,705**, rehabilitation fund Level 2 **34,617**, short-term investments Level 2 **137,867**, and FY25 rehabilitation fund Level 2 **29,118**, each repeated as its row total. These rows are absent from p.36 storage. Only the final hierarchy row survives as IDs **9948/9949**: label **`Derivative financial liability – (1,848)`**, values **dash/(1,848)**, generic `col0/col1`; its four Level1/Level2/Level3/Total positions were not preserved. The remaining 12 cells in this region are the separate Note 21 commitments table. A page-level “unverified” designation is insufficient disclosure of an almost entirely dropped hierarchy.

### B1 — segment-column semantics

Visually inspected all four page headers, pp.21–24. The eleven **main-grid** columns are correctly ordered: Barberton, Evander, Solar, MTR, Tennant, Mining operations, Exploration, Agricultural ESG, Corporate, Funding, Group. On p.21 **594 is directly beneath Agricultural ESG projects**, aligned with that column's cost **(1,187)** and other entries; Corporate is the next column to its right. No economic inference from blueberries is needed. This confirmation does not extend the grid semantics to the geographic table below it (F001).

### B2 — reproducible random page-attribution sample

Sample: Python `random.Random(20261029).sample(SELECT * FROM cells ORDER BY id, 5)`; full records saved in `codex_evidence/samples.json`. Each glyph was located visually on its stated physical page. **No attribution findings in these five cells.**

| Stored cell ID | Stated page | Printed row / glyph | Result |
|---|---|---|---|
| 9790 | 32 | Northern Territory loan, FX movement FY26 **540** | Match |
| 9046 | 19 | FY25 dividend paid, retained earnings **(27,459)** | Match |
| 2799 | 23 | FY25 Evander Mining **(23,882)** | Match |
| 5322 | 41 | FY25 Group all-in costs **469.3 US$m** | Match |
| 9188 | 25 | Contract liability non-current portion FY26 **dash** | Match |

### B3 — investing signs

Physical p.18: IDs **2295**, **2297**, **2301**, FY26 payments for PPE **(189,723)**, exploration **(26,030)** and other intangibles **(390)**, respectively store **−189723, −26030, −390**. All three match printed brackets; no sign finding in this sample.

### B4 — unexecuted identities and correction to the earlier reviewer

The previous review correctly flagged missing tests for pp.29/35 but overstated the completeness of their stored rows. More importantly, its description of Note 19 as a bridge directly to **556,991** is incorrect: the note's printed final subtotal is **712,119**, before dividends, tax, royalties and net finance costs. The further deductions appear on p.18. Independent calculations executed and saved:

- FY26 adjustments **143,482**; **534,368 + 143,482 = 677,850**; working capital **46,559**; **677,850 + 46,559 − 18,200 + 8,030 − 1,873 − 247 = 712,119**; then **712,119 − 58,540 − 74,135 − 12,112 − 14,987 + 4,646 = 556,991**.
- FY25 adjustments **30,079**; **196,633 + 30,079 = 226,712**; working capital **−2,113**; **226,712 − 2,113 − 9,600 + 8,422 − 5 − 232 = 223,184**; then **223,184 − 23,675 − 20,147 − 4,887 − 21,439 + 1,824 = 154,860**.

These are reviewer calculations; they do not retroactively add coverage to the build's suite. Earliest demonstrated failure for F001–F005 is extraction/storage; subsequent review/coverage reporting failed to distinguish missing data from present but untested data. No specific downstream valuation impact was established, and no target or recommendation was reviewed.

## 3. Pass C result

Read only the two requested historical database blobs, using `git show <revision>:<database path>`; did not read commit messages or other history. `8dc69c6` contains **2,436** cells across **13** regions; `71124ab` contains **4,802** across **40** regions. **No existing region shrank between these endpoints**; all 13 original region counts are identical. Counts are saved in `codex_evidence/history_counts.json`. This endpoint comparison cannot establish that no intermediate rebuild temporarily reduced coverage, or detect equal-count row substitutions.

## 4. The one thing the build is most likely still getting wrong

It treats a page's surviving numeric tokens as table coverage, silently dropping differently shaped sub-tables and assigning surviving values to the preceding table's columns.

### Coverage, handoff and limits

Source renders actually inspected: physical **18, 19, 21–25, 29, 32–36, 41, 44, 46**. Native text was extracted for pp.17–50; that inventory is not a claim of exhaustive visual or cell-by-cell review. Other pages, all 97 conflict explanations, the Excel view, and every unchanged test assertion were not independently validated. The prior self-authored `reviews/20261029T*` reviews and scoring fixture were not used. The supplied Gemini-role review, consolidated brief, coverage file, relevant workplan and remediation/test sources were inspected; no paid model calls or production changes occurred.

Required next work: restore distinct table schemas and missing rows, preserve source glyphs, then execute the identities above and refresh table-level coverage. Proposed reusable lesson: test inventory completeness separately from arithmetic consistency; a passing sum over a narrowed dataset cannot validate omitted rows. Proposed only: no prompts, guardrails or SQLite questions were changed, and no demonstrated DeepSeek improvement is claimed. The versioned section 1A audit, input preservation and calculations are linked from `codex_evidence/audit_location.txt`.
