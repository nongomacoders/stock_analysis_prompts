# Logical PDF capture change

Implemented a local page-level planner for new automatic captures. It identifies
native statement/note/subtopic headings, recognizes observed reporting-period and
instrument changes, groups small related note material, and falls back to bounded
page/character budgets. No model calls or financial reruns were made.

| Source | Physical pages | Budget-only groups on the same partition | New logical groups | Largest group |
|---|---:|---:|---:|---:|
| NTU1H26 |38|9|30|3 pages|
| DCP FY26 AFS |87|28|70|5 pages|
| PAN FY26 results |54|24|26|6 pages|

All179 physical pages were included exactly once; all source hashes and the
production database fingerprint matched the pre-validation baseline. More groups
can increase paid call count. These offline results establish coverage and wiring,
not lower cost, shorter model time or better financial accuracy.

Review [NTU_plan.md](NTU_plan.md), [DCP_AFS_plan.md](DCP_AFS_plan.md) and
[PAN_plan.md](PAN_plan.md). Their JSON companions retain exact source hashes,
native heading evidence, boundary reasons and continuation dependencies.
The previews follow the one-shot range partition and same planner as capture.

NTU examples: separate primary statements; debt and facilities together on14–15;
principal-portfolio ECL on24; trade-receivable ECL on25. Page25 also starts currency
risk, so the whole page remains intact with an explicit link to26. Page26 starts
fair value and links to27. Same-period segment statement/reconciliation pairs stay
together. Explicit dates separate current/prior-year groups when detected.

Defaults: target3 pages/12,000 extracted characters, hard6 pages/24,000 characters;
same-heading continuations can extend to the hard limit. Oversized single pages
stay intact with a warning. Whole-page capture avoids cutting on-page tables and
footnotes, but cross-page/mixed-topic material still needs review. Missing headings
or OCR-only content use an explicitly qualified fallback. Detailed font metadata
is not repeatedly injected into prompts.

Final full suite: **214 passed in70.22s, exit0**, with Python networking denied.
Actual receipts and earlier failed/repaired checks are retained under `validation/`.
An integration fixture initially assumed one request meant one saved package;
another mocked only part of a full PDF while testing orchestration. Fixtures now
model the intended scope. The shared-page regression fixture initially overlapped
its heading and body text; corrected geometry, with real NTU pages24–25 visually
checked. No test or model-output failure is hidden as success.

See [implementation_record.json](implementation_record.json),
[cleanup_status.json](cleanup_status.json) and [LOGICAL_CAPTURE.md](../../../docs/LOGICAL_CAPTURE.md).
All seven task-created test directories were removed after preserving results.
Original captures and valuations were not migrated; new captures use the planner.
