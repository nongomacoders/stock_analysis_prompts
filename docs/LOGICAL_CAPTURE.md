# Logical and manageable PDF captures

Automatic capture should present a coherent evidence task: a statement, note or a
small related set of tables and explanations. Page counts alone do not identify
those tasks. This planner refines the existing major-section map locally, without
calling a model or changing the original PDF.

## Boundary decisions

1. Read native word text, font sizes and positions. Ignore small running headers,
   footers, table dates and isolated large note numbers beside small column labels.
   Keep the observed heading text/position as navigation evidence.
2. Prefer specific statement/note/subtopic headings near the page top. Normalize
   “continued” for matching, including mixed-font continued suffixes. Recognize
   observed body-period labels; do not guess dates from printed page numbers.
3. Split distinct statements and unrelated notes. Small parent/child notes can stay
   together. Different explicit reporting periods and principal-portfolio versus
   trade-receivable headings separate tasks even inside one broad credit-risk note.
4. Use three pages/12,000 extracted characters as the fallback/related-topic target,
   with hard defaults of six pages/24,000 characters. A coherent repeated heading
   can continue beyond the target to the hard limit. Caller-supplied limits remain
   supported. These are source-text limits, not a guaranteed full-prompt token budget.
5. Keep each physical page intact. A single oversized page is retained with a
   warning. Several notes can share one page; retain all of it rather than cutting
   away a table, footnote or the next note's introduction. Link an observed note
   start on the shared page to its next-page continuation. Flag forced size cuts
   similarly, carrying related evidence requests as `Pending: [section/pages]`.

The one-shot pipeline first gives each physical page one owner among overlapping
detected ranges, preferring the narrower/deeper range, and explicitly retains gaps.
It does not discard the other overlapping titles. Manual partial captures keep
their existing semantics; they do not claim whole-report completion.

## Saved provenance and prompts

`capture_coverage` retains parent/requested/actual ranges, all chunk spans, logical
heading, boundary reason, continuation flag/reason, prior/next chunk pages, applied
limits, source characters, sparse pages and native heading observations. Physical
pages start at1. Printed labels remain unset unless explicitly supplied.

Saved package titles show the logical heading and actual page range. Subheadings
use the existing report-map/section-ID mechanism. Detailed font observations stay
in local metadata; prompt coverage remains compact and explicitly warns about
continuations. Source text is unchanged by planning. The single-package API still
returns the first saved package; all packages are saved and queued from SQLite.

Existing captures, model outputs and valuations are not migrated or rerun by this
change. New automatic captures use the planner. An intentional recapture remains
separate from reusing a completed analysis.

## Review the plan without model charges

Run from the repository with the local environment:

```powershell
.venv/Scripts/python.exe workflow/changes/20261028_logical_capture/preview.py
```

This produces Markdown/JSON previews for NTU, Dis-Chem's AFS and PAN under that
changes folder. They list physical pages, observed topics, source characters,
boundary reasons and continuation flags, with source hashes. The preview disables
Python networking, performs no production database writes and verifies unchanged
source PDFs/database. It uses the same planner; it does not generate analysis.

## Limits and evaluation

This is a conservative native-layout heuristic, not OCR or a semantic table parser.
Unusual fonts, weak/missing headings, multi-column spreads or a topic change inside
a page can require human correction. Cross-page references/footnotes still need
the question ledger and independent review. No detected boundary proves a company
disclosure is complete, or that a model will finish or reason correctly.

More focused captures can create more model calls. Offline coverage and regression
tests establish page preservation and integration; they do not establish improved
financial accuracy, latency or total spend. Measure those in a separately authorized
controlled model trial with complete per-call accounting.
