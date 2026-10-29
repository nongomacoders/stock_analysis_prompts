# Codex-role review — PAN agentic report build

**You are the second gate.** A Gemini-role reviewer already audited this build and produced
`reviews/p4_review_pack/INDEPENDENT_REVIEW.md`. Five of its findings were remediated in commit
`71124ab`. Your job is not to repeat that pass — it is to check it against the source PDF, and to
find what a database-level reviewer structurally cannot see: **misread columns, wrong page
attributions, and tables claimed as covered but never actually read.**

## Environment

Open this folder as the project:

```
C:\Users\diond\Desktop\Projects\stock_prompts_agentic
```

You do **not** need a venv to review. Python's stdlib `sqlite3` is enough:

```python
import sqlite3
con = sqlite3.connect("workflow/changes/20261029_agentic_report_build/build/report.sqlite")
```

If you want to run the suite (optional, it should already pass):

```
C:\Users\diond\Desktop\Projects\stock_analysis_prompts\.venv\Scripts\python.exe -m pytest tests_reconcile -q
```
(cd into `workflow/changes/20261029_agentic_report_build` first.)

**Source PDF** (unchanged, hash-verified):
`companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf`
SHA-256 `62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd`, 54 physical pages.

## Ground rules

1. **Read the PDF and the database. Do not review git history** except for one thing (λ below).
   Commit messages are the author's assertions, not evidence.
2. **Do not trust the previous reviews** in `reviews/20261029T*` — they are self-authored role-play by
   the same agent that built this. Treat them as drafts.
3. Report findings with: page number, the printed glyph, the stored cell, and severity
   (wrong / missing / mislabelled / unverifiable).

## Pass A — verify the remediation of the Gemini findings

Commit `71124ab` claims five fixes. Check each against the PDF, not against the commit message:

1. `document` is now the SHA-256 for all 4,800 cells (was a Windows path for 1,196). Verify by query.
2. p.34 Note 18 rows recovered: `[14] Ordinary shares to be issued … 148,218` and
   `[7] Property, plant and equipment … 142,436`. **Verify on the PDF that these are the right labels
   and values**, and that the note reference numbers are 14 and 7.
3. Brief figures now asserted: EPS 17.60/7.16, TCI 400,965/155,554, levered FCF 201.8, net cash
   (185.7), net senior (194.7), segment revenue cells. Check the printed values on pp.18, 22, 46 and 21.
4. The ledger table now shows all eight questions as open. Check the `questions` table agrees.
5. p.33 Note 17.1 share-based roll-forward: opening 21,486 + movements = closing 64,352. Verify the
   movement lines on the PDF, especially whether an FX line exists that the test may be silently
   summing in the wrong direction.

## Pass B — the checks only you can do against the PDF

1. **Column semantics.** For pp.21-24 (Note 3), confirm the eleven columns are what the build says:
   Barberton, Evander, Solar, MTR, Tennant, Mining operations, Exploration, Agricultural ESG,
   Corporate, Funding, Group. In particular: is the `594` revenue really in Agricultural ESG and not
   Corporate? The build justifies this by geometry plus a blueberries cross-reference on p.25 —
   that is weaker than it sounds if both columns are otherwise zero.
2. **Page attributions.** Pick any five cells at random and confirm the stated `physical_page` is where
   that glyph actually prints. Off-by-one page errors would be invisible to a database reviewer.
3. **Sign conventions.** Cash-flow outflows are printed in brackets and stored negative. Spot-check
   three investing lines and confirm the sign in `value_num` matches the printed bracket.
4. **Tables claimed but not covered.** Read pp.29 and 35 (Note 8 capex, Note 19 profit-to-cash bridge).
   The build marks these `[printed, unverified]`. Confirm that label is honest — i.e. that the rows are
   in the database but genuinely have no executed check — and say whether an identity exists that
   should have been executed.
5. **Anything the build silently omits.** Look for a printed table in pp.17-50 that is neither in the
   database nor declared as prose/no-figures. This is the highest-value finding you can produce.

## Pass C — one history check (λ)

The build rewrote several regions from scratch. Confirm no rebuild ever *reduced* coverage without
recording it: compare `SELECT table_region, COUNT(*) FROM cells GROUP BY 1` between `8dc69c6` and
`71124ab`. A region that shrank without a deferral note is a finding.

## Known limits — declared, do not spend effort re-finding

- **13 pages are extracted with printed values and lineage but no executed identity**: pp.4, 6, 9, 10,
  19, 26, 29, 30, 31, 34, 35, 36, 39. `fiscal_year` is NULL and `column_index` is printed position for
  those rows. The brief marks them `[printed, unverified]` and claims no conclusion rests on them.
- **pp.37, 38, 51** carry no figures (contents, prose, glossary).
- **97 conflicts are recorded, not resolved** — that is deliberate (charter covenant 1).
- **p.34's Emmerson acquisition bridge is incomplete**: 11,879 and 160,097 are not in the text layer
  where the build looked. If you can find them printed, that is a real find.

## Output

Write to `reviews/p4_review_pack/CODEX_REVIEW.md`. Structure:

1. **Verdict on the five remediations** — correct / incorrect / unverifiable, each with evidence.
2. **Pass B findings** — one line per finding, with page, glyph, stored cell, severity.
3. **Pass C result** — did any region shrink silently.
4. **The one thing the build is most likely still getting wrong**, in a sentence.

Do not write prose praise. If everything you checked is correct, say "no findings in the areas
checked" and list what you did not check.
