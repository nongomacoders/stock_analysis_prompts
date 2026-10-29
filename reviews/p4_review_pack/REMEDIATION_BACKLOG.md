# Remediation backlog — Codex source-evidence review

Source review: `reviews/p4_review_pack/CODEX_REVIEW.md` (second gate, against the PDF).
Every finding below was re-verified against `build/report.sqlite` before acceptance.

**Verdict: accepted in full.** The Gemini-role pass checked the artifact against itself; Codex
checked it against the document, and found that the generic note parser treated *surviving numeric
tokens as table coverage* — dropping differently shaped sub-tables and mislabelling what survived.

## Verified defects

| ID | Page | Defect (re-verified) | Status |
|---|---|---|---|
| **F004** | 34 | `11,879` and `160,097` absent from the database — **and I told the user they were unavailable in the text layer. That was wrong.** Codex re-extracted the text and found both printed. | **Confirmed** |
| **F002** | 29 | None of Note 8's six totals (`21,832 / 202,163 / 223,995` and `11,626 / 156,283 / 167,909`) exist on p.29. Only 18 of 54 amount positions survive. | **Confirmed** |
| **F001** | 24 | The Geographical information table's three FY25 leaves (`740,819 / 155,716 / 445`) are stored under `note3_segment_analysis` with `column_label='Solar projects'`, and the footnote block is absorbed into the first row label. FY26 cells and FY25 total missing. | **Confirmed** |
| **F003** | 35 | Note 19 row `(Increase)/decrease in other receivables (21,206) / 2,833` absent, so working capital 46,559 cannot be rebuilt from stored leaves. | **Confirmed** |
| **F005** | 36 | Note 20.2 fair-value hierarchy (`12,705 / 34,617 / 137,867 / 29,118`) absent; only a mangled derivative row survives. | **Confirmed** |
| **Count** | — | Database holds **4,802** cells, not 4,800. Brief and audit carry the stale figure. | **Confirmed** |

## What Codex confirmed as correct

- All five remediations are correct within their narrow claims (`document` normalised, the two Note 18 rows recovered, headline constants asserted, all eight questions open, Note 17.1 roll-forward sums with FX 2,331/438).
- **Column semantics**: on p.21 the `594` revenue sits visually beneath Agricultural ESG — my geometry assignment was right and the blueberries inference was unnecessary.
- Five random page attributions all matched; investing-bracket signs all matched.
- No region shrank between `8dc69c6` and `71124ab`.
- It also corrected the *Gemini* review: Note 19's printed subtotal is **712,119**, not 556,991; the further deductions to 556,991 print on p.18.

## Root cause

The generic note extractor (`extract_pan_notes.py`) selects the modal column count per page and keeps
only rows at that width. Any sub-table on the same page with a different shape is silently dropped, and
its surviving numbers are attributed to the preceding table's columns. This is the failure mode the
build's own p.28 experience foreshadowed — and the model-width filter I added to fix p.34 is the same
mechanism that ate Note 8.

## Fix approach (not yet implemented)

1. **Per-table schemas, not per-page.** Identify each sub-table by its printed heading and derive
   columns per table; never assume one width per page.
2. **Completeness test separate from arithmetic.** The reusable lesson Codex proposed: assert that the
   number of amount positions stored for a table equals the number printed. A passing sum over a
   narrowed dataset cannot detect omitted rows.
3. **Restore and reconcile, in this order**: F004 (both acquisition bridges), F002 (Note 8 three-column
   table), F003 (Note 19 with 712,119 as the real subtotal), F001 (geography as its own region),
   F005 (hierarchy).
4. Refresh the coverage file and the brief's count once extraction is actually complete.

## Note on provenance

These are reviewer findings, verified by the build author against the same database; they are not yet
demonstrated improvements. No prompt, guardrail or SQLite question was changed by this review.
