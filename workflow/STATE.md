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
  - Pre-populated and updated the PAN FY2026 questions ledger (`documents/questions/62b10bcd.../questions-ledger.md`) after Section 1 (`01-D002-KEY-F26-FEATURES-...`) and Section 2 (`02-D003-Chief-executive-officer-s-statement-...`).
  - Defaulted `CaptureWindow` save folder to the opened PDF's parent directory (`candidate.path.parent`) and prefixed saved section folders/ZIPs with the sequential capture number and report map section ID (`01-D002-...`, `02-D003-...`).
  - Removed `/captures/` and `/documents/` from `.gitignore` so all captures, section maps, and stored question ledgers stay tracked in Git across computers.

## Next steps

1. Open `Run Capture.cmd` and load `Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf`—the save folder automatically defaults to `company_results/PAN/FY-2026/` and `Stored questions` holds the open questions after Section 2 (`D003`).
2. Capture Section 3 (e.g., `D005/D006` financial statements & notes or `D008 Alternative performance measures`); it will automatically save as `03-D008-...` (or `03-D005-...`) in `company_results/PAN/FY-2026/`.
