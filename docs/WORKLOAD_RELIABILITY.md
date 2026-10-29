# Capture coverage and persistent questions

Implemented 2026-10-28 after the workload review. This change addresses capture
coverage and question-ledger reliability; it does not add analytical guardrails or
change DeepSeek's reasoning policy.

## Automatic capture

`auto_capture_section` now uses the local logical-page planner described in
[LOGICAL_CAPTURE.md](LOGICAL_CAPTURE.md). It prefers native statement/note/subtopic
headings, distinguishes observed reporting periods and selected instrument types,
and keeps related parent/child notes together when small. Unknown headings use a
three-page/12,000-character fallback target; hard default limits are six pages or
24,000 extracted characters. A single page remains intact even above the character
limit, with a warning. No source text is truncated.

Whole-page capture preserves on-page tables/footnotes. It cannot guarantee an entire
multi-page table stays together. Size cuts and observed shared-page note continuations
are flagged and linked to the neighboring capture. For example, a trade-receivables
table and the start of currency risk can share a page; that page stays whole and the
next currency-risk capture is explicitly referenced. A capture boundary is not a
missing-disclosure claim. Native headings are a reviewable draft, not semantic proof.

Every chunk records its parent heading, requested range, clamped document range,
all chunk spans, its actual pages and sparse-text warnings in `capture_coverage`.
Logical headings, boundary reasons, native font/position observations, source
character counts and previous/next chunk pages are also saved. Verbose font
observations remain local; compact coverage and continuation instructions reach the
prompt. New logical captures register subheadings in the existing report map.
The existing single-package API returns the first saved package; consumers queue
all packages from SQLite. Requested pages outside the physical document are
explicitly flagged. A capture failure stops automatic ingestion instead of silently
continuing past a missing section. Coverage describes captured page presence,
not financial verification, OCR quality or completeness of the section detector.
The one-shot pipeline partitions overlapping detected ranges before capture and
retains unclassified gaps, so each physical page has one automatic owner. Explicit
manual selections/comparison-dialog ranges can still overlap intentionally.
The automatic pipeline persists its requested page ranges before capture. A cached
prefix from an interrupted capture cannot be reused as a completed plan; missing
pages require an explicit recapture, preserving the existing partial material.

## Structured ledger contract

New automatic captures and sequential resubmissions use `ledger_contract=1`.
Explicit callers can opt in through `save_package(..., ledger_contract=1)`;
legacy captures without the marker retain their existing read/save behavior.
The section template is adapted at construction so Section 4 requests one JSON
delta with `ledger_version`, `updates` and `new_questions`, rather than a full
rewritten ledger. Exact submitted prompts remain stored on the section.

SQLite stores stable question IDs in `ledger_questions`, their revisions in
`ledger_events`, and raw accepted/rejected response attempts in
`section_response_attempts`. Existing unstructured ledgers are preserved verbatim
as an open legacy request. That aggregate cannot be closed automatically; it
requires review and decomposition, avoiding accidental closure of many items
with one citation. New questions have explicit target document/section, evidence
requirements and closure conditions. Omitted questions persist. Identical question
text is deduplicated; semantic duplicates can still require review.

Each section receives at most 12 open questions, ranked by target document,
section, evidence-text relevance and priority. The prompt retains evidence
requirements and closure conditions but omits copied answer narratives. Unsent
questions remain open; Stage 1 receives the complete ledger. This bounds each
section's task without treating omitted questions as resolved. Routing is a simple
heuristic and can miss a useful question, which remains visible to Stage 1/review.

Updates use open/partial/contradicted/resolved status. Evidence-backed statuses
require the current source SHA-256, a captured physical page, and a literal excerpt
present in that page's captured text. Whitespace may vary; words, signs and numbers
must match. Resolution also needs an answer. This checks presence and provenance,
not whether the excerpt logically supports the answer or satisfies its closure
condition. Independent review remains mandatory.

Malformed deltas and unsupported evidence are rejected atomically. The response
attempt is preserved, questions are unchanged, and automatic processing stops with
a visible error. Valid empty updates are allowed, and an empty open ledger is
rendered explicitly without deleting closed question history. Parent/companion
reports share the same question state. Manual text edits are preserved as additional
legacy evidence requests rather than silently dropping persistent records.

## Two-company comparison

NTU 1H26 and DCP FY26 are rerun in versioned evaluation directories with isolated
databases and complete source-page coverage. Original production outputs, source
PDFs and database remain preserved. Exact requests, raw responses, rejected
attempts, repairs and metadata are saved. This is a combined coverage/ledger
comparison, not a controlled reasoning-only experiment.

Comparison-only recovery limits are recorded separately from production policy:
one 32,768-token retry for an exhausted section, and up to 98,304 completion tokens
for an exhausted full stage. NTU's full Stage 2 still exhausted both budgets. It
therefore has a separately labeled, concise WITHHELD recovery brief, generated at
the ordinary section reasoning setting, rather than a completed full valuation.
That scope/settings difference must not be reported as evidence that the full
valuation improved or completed. Production stage reasoning/budgets remain unchanged.

Live trials exposed non-literal model quotations despite the new contract. The
comparison runner allows one preserved JSON-only repair. If its evidence updates
still fail, the runner can produce an explicitly labeled local open-only fallback:
all existing questions remain open and narrative closure claims are qualified;
only valid new questions are accepted. Raw candidates are retained. This experiment
fallback is not the production app's behavior, and must be counted separately
when measuring model compliance and repair cost. It is not evidence that DeepSeek
successfully answered the rejected questions.

DeepSeek alone runs through OpenRouter. The user runs Gemini evaluation in
Antigravity using the prepared evidence pack; no Gemini OpenRouter calls are
authorized. Codex reviews Gemini's preserved result after it is supplied. No new
valuation is considered financially validated merely because generation or the
publication gate succeeds.
