# Review pack — agentic report build P4 (PAN, six sections)

**Purpose.** Hand this to a Gemini-role reviewer (Antigravity) and then a Codex-role reviewer. The
intent is an *independent* check of a build whose own suite is green — the interesting question is not
"does it add up", it is "what did the suite fail to look at".

**Commit under review**: `636be8a` on branch `agentic-report-build`.
**Diff**: `git diff 7cec693^..636be8a -- workflow/changes/20261029_agentic_report_build/`

---

## 1. What to read, in this order

| # | File | Why |
|---|---|---|
| 1 | `workflow/changes/20261029_agentic_report_build/CHARTER.md` | the covenants the build claims to obey |
| 2 | `READING_BRIEF_CONSOLIDATED.md` | the artifact being reviewed |
| 3 | `build/report.sqlite` (tables `cells`, `conflicts`, `questions`) | the evidence behind every figure |
| 4 | `tests_reconcile/` (5 test modules) | what is actually executed |
| 5 | `WORKPLAN*.md`, `HYPOTHESES.md` | what was planned vs deferred, and why |

Source PDF (unchanged): `companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf`,
SHA-256 `62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd`.

---

## 2. Questions for the Gemini-role pass (adherence and self-consistency)

1. **Covenant 1 — never replace a printed figure.** Find any place where the brief or code substitutes a
   value rather than recording a conflict. Anchor to check: the brief says substituting 84,929 for 94,929
   makes an identity tie and calls that "conditional agreement only". Is that discipline held everywhere?
2. **Covenant 2 — arithmetic in code.** Is any number in the brief asserted without a corresponding test
   assertion? Spot-check three figures of your choosing against `tests_reconcile/`.
3. **Covenant 3 — lineage.** Does every cell in `cells` carry page, document hash and extraction commit?
   Are the unverified pages labelled as such in the brief?
4. **Covenant 4 — ledger independence.** Are the six open questions genuinely open, or has arithmetic been
   used to close a definitional question?
5. **Honesty of the defect log.** Two extractors were written, failed and reverted (p.44 first attempts,
   p.28 first attempt). Is the recorded reasoning plausible, or is it constructed after the fact?

## 3. Questions for the Codex-role pass (against the PDF)

1. Open pp.48-50. Verify five printed figures of your choosing appear in `cells` with identical glyphs,
   including any `–` nil cells.
2. Open pp.17-18. Verify the balance sheet and income statement anchors, and confirm closing cash
   108,312 appears on both the balance sheet and the cash flow statement.
3. Open pp.21-24. Verify that the segment columns sum as the suite claims, and check whether the brief
   mislabels any column.
4. Open pp.44-47. Verify the Adjusted EBITDA 142.5 (p.45) versus 142.4 (p.50) claim, and the ROCE
   inputs.
5. **Adversarial**: find a printed table in this document that the build claims to have covered but did
   not, or a total the suite should have checked and did not.

---

## 4. Known limits, declared up front (do not spend review effort re-finding these)

- **Thirteen pages are extracted but unverified** — printed values and lineage, no executed identity:
  pp.4, 6, 9, 10, 19, 26, 29, 30, 31, 34, 35, 36, 39. The brief marks them `[printed, unverified]`.
- **Pages 37, 38, 51** carry no figures (contents, prose, glossary).
- **The column semantics of the unverified notes are not established** — `column_index` is printed
  position, and `fiscal_year` is NULL for those regions. This is a real weakness, not a stylistic choice.
- **97 conflicts are recorded, not resolved.** Two are material: the Adjusted EBITDA scope difference
  (663.1 vs 609.4) and the Barberton 10,000 oz gap.
- **No external model reviewed this build before you.** Prior "Gemini"/"Codex" files in `reviews/` are
  self-authored role-play and should be treated as drafts, not as evidence of independent review.

## 5. What a good outcome looks like

Not "the numbers are right" — the suite already establishes that within its coverage. The useful output is
a list of: figures checked *outside* the suite's coverage; tables present in the PDF but absent from the
build; and any place where the brief's confidence exceeds its evidence.
