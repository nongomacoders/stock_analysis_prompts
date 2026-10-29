# Runbook: first agentic report build (one session, one section)

Branch: `agentic-report-build` (worktree `C:\Users\diond\Desktop\Projects\stock_prompts_agentic`).
Read `CHARTER.md` first. All rules there bind any session working in this worktree.

## Preparation

- Source PDF (unchanged, hash-verified): `companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf`
  (`62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd`). Physical pages 48-50.
- Python environment: the worktree has no `.venv`. Run everything with the main checkout's
  interpreter: `C:\Users\diond\Desktop\Projects\stock_analysis_prompts\.venv\Scripts\python.exe`.
  Test root/basetemp inside the worktree only (`tmp/<unique-task>`), never the main tree.
- Ground truth for the reconciliation suite: `ground_truth/pan_d009_expected.json`.
- Reference to the warning: never let a session "correct" a printed number (covenant 1).

## Phase order (commit after every phase)

1. **P0** Write `WORKPLAN.md` in `workflow/changes/20261029_agentic_report_build/`:
   schema sketch, list of cells expected from pp.48-50, ledger imports. Commit.
2. **P1** Build extraction: `report.sqlite` under `workflow/changes/20261029_agentic_report_build/build/`
   (gitignored in bulk? No — the DB is small; commit it with a manifest row-count receipt).
   Extraction scripts live in `build/extraction/`. Every cell: value, unit, physical page,
   printed label, row/col, source sha256. Run a render-and-look pass (pypdfium2 +
   `PySide6.QtWidgets.QApplication`, `PySide6.QtGui.QImage`) to eyeball dense tables; the
   renders go to evidence storage, referenced from receipts, not committed in bulk.
   Commit with the row-count receipt in the message.
3. **P2** `tests_reconcile/` pytest suite driven by the ground-truth identities. Gate:
   green, or every failure recorded in the `conflicts` table with citations before the
   commit completes. Commit.
4. **P3** Hypothesis branches (each `git worktree add`): default branch keeps printed
   values; alternative branches explore component reinterpretations only. Suite runs on
   each; merge criterion per charter section 2/3. Commit per branch; record branch ledger.
5. **P4** Generate the reading brief/report and an Excel view (`openpyxl`) strictly from
   `report.sqlite`. Commit.
6. **P5** Freeze the artifacts; hand the P0-P4 diff to a Gemini-role review session, then a
   Codex-role review against the PDFs. Preserve both outputs under
   `reviews/<UTC timestamp>_<reviewer>/`.
7. **P6** §1A-shaped audit: input manifest (every read file + sha256), inspected pages/
   renders, executed checks + exit codes, findings (supported/failed), cost/time if any
   model calls were made, limitations. Update the branch-local `workflow/STATE.md`.

## Definition of done (first run)

- Suite green with every known conflict recorded (not "fixed").
- Zero covenant-1 violations in the audited diff.
- Detection score: all marked identity checks from the ground truth reproduced
  independently (not seeded as test answers the agent was told to "find" — the suite is
  generated from the DB/schema, the fixture is only the scoring key used by the reviewer).
- Review records P5 + audit P6 saved; branch `STATE.md` updated; production untouched.

## Prohibited

- Writing to `companies/**/sources/**` or any production table.
- Model-performed arithmetic in the report prose (covenant 2).
- Silently expanding scope beyond section D009 pp.48-50.
- Copying bulk PDFs or page renders into git (refer them from manifests instead; avoid
  long-path commits — one `Filename too long` warning already occurred at worktree setup).
