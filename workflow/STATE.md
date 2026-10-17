# Current state

Last updated: 2026-10-17 (Africa/Johannesburg).

## Objective and boundary

Analyze and forecast from company presentations and reports section by section without whole-PDF inaccuracies or narrative fluff:
1. Scan the PDF locally for major sections (`section_capture/report_map.py`).
2. Capture a section in the PySide6 app (`section_capture/`). The LLM gives **no narrative commentary**—instead, it deeply scrutinizes footnotes that contain commentary, draws up verification questions for future sections (`D001`–`D013`), and records compact baseline forecast numbers.
3. Store those open questions in the app's **Stored questions** ledger (`documents/questions/<sha256>/questions-ledger.md`).
4. Capture the next section: the app automatically embeds the stored questions into `prompt.md`, and the LLM answers **only** the stored questions that relate to that section, draws up new questions from that section (and its footnotes), and outputs an updated open-questions ledger for the next section.

## Completed

- **Implemented progressive Stored Questions Ledger & deep footnote scrutiny**:
  - Updated `prompts/mining/12-analyst-reading-brief/v1.1.0/prompt.md` and `prompts/mining/00-report-orientation/v1.0.0/prompt.md` to eliminate narrative commentary essays, enforce high-effort analysis of footnotes with commentary (`[^1]`, etc.), answer only stored questions relating to the current section, and output a copy-ready **Updated Open Questions Ledger**.
  - Added `QuestionsLedgerDialog` (`section_capture/map_dialog.py`), `load_questions_ledger` / `save_questions_ledger` (`section_capture/report_map.py`), toolbar/sidebar **Stored questions** controls (`section_capture/window.py`), and automatic embedding of `stored_questions` into `prompt.md` and `stored-questions.md` (`section_capture/packages.py`).
  - Pre-populated the PAN FY2026 questions ledger (`documents/questions/62b10bcd.../questions-ledger.md`) with the 8 open verification questions from Section 1 (`KEY F26 FEATURES`, including the MTR footnote `[^1]` H1 calcine constraint and the `2,436.3m` vs. `2,029.6m` dividend share-count gap) and updated the Section 1 capture pack in `company_results/PAN/FY-2026/20261017-151815-KEY-F26-FEATURES-8d715d1f/`.
  - Removed `/captures/` and `/documents/` from `.gitignore` so all captures, section maps, and stored question ledgers stay tracked in Git across computers.

## Next steps

1. Open `Run Capture.cmd` and load `Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf`—you will see `Stored questions (9 lines)` already loaded from Section 1 (`KEY F26 FEATURES`).
2. Capture Section 2 (e.g., `D003 CEO's statement` or `D008 Alternative performance measures`) and click **Save section + upload ZIP**—the 8 stored questions from Section 1 will be automatically embedded in `prompt.md` so the LLM answers only the ones relevant to Section 2 and draws up new questions for the remaining sections.
