# Current state

Last updated: 2026-10-17 (Africa/Johannesburg).

## Objective and boundary

Analyze and forecast from company presentations and reports section by section without whole-PDF inaccuracies or narrative fluff:
1. Scan the PDF locally for major sections (`section_capture/report_map.py`) and store the report metadata, section map, and open questions ledger in the central SQLite database (`documents/analysis.sqlite`).
2. Capture a section in the PySide6 app (`section_capture/`). Saving stores `selected_text`, `selections_json`, `stored_questions_snapshot`, `prompt`, and `manifest_json` directly in SQLite (with no `.png` image crops, section folders, or `.zip` archives) and automatically copies `prompt` to the system clipboard.
3. Paste the prompt into the LLM. The LLM gives **no narrative commentary**—it answers only stored questions targeting the current section, scrutinizes footnotes with commentary (`[^1]`, etc.), draws up verification questions for future sections (`D001`–`D013`), and outputs an **Updated Open Questions Ledger**.
4. Store the LLM response in **Saved sections / LLM response** (`SavedSectionsDialog` in `section_capture/map_dialog.py`) or update **Stored questions** directly; pasting the LLM response automatically extracts Section 4 (`Updated Open Questions Ledger`) into `reports.questions_ledger` in SQLite for the next section capture.

## Completed

- **Central SQLite persistence (`documents/analysis.sqlite`)**:
  - Created `section_capture/db.py` with `reports` and `sections` tables storing `report_map_json`, `questions_ledger`, `selected_text`, `selections_json`, `stored_questions_snapshot`, `prompt`, `llm_response`, and `manifest_json`.
  - Updated `section_capture/report_map.py`, `section_capture/packages.py`, `section_capture/map_dialog.py`, and `section_capture/window.py` to persist all maps, questions ledgers, captured sections, prompts, and LLM responses exclusively in SQLite without writing `.png` or `.zip` files.
  - Added `SavedSectionsDialog` (`Saved sections / LLM response`) to inspect any captured section's prompt, paste/save the LLM response in SQLite, and automatically extract Section 4 (`Updated Open Questions Ledger`) into `reports.questions_ledger`.
  - Added editable `HeadingComboBox` dropdown for **Section heading**, retained the main heading after saving a subsection (`D005.1`, `D006.1`), and blocked saving a blank `Sub-heading` once a section has subsections.
  - Migrated PAN FY2026 report map, 16-question open ledger, and all 4 captured sections (`01-D002`, `02-D003`, `03-D005.1`, `04-D006.1`) into `documents/analysis.sqlite` and removed legacy filesystem capture folders, `.png` crops, `.zip` archives, `documents/maps/`, and `documents/questions/`.

## Next steps

1. Open `Run Capture.cmd` and load `Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf`—the app loads the report map, existing sections (`01-D002` through `04-D006.1`), and the 16 open questions from `documents/analysis.sqlite`.
2. Continue capturing `Financial notes` subsections (`D006.2`, `D006.3`, etc., e.g. Note 3+, Note 6 tax, Note 13/16 cash & debt, Note 14/15/18 shares & Emmerson acquisition) or `D008 Alternative performance measures`.

