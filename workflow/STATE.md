# Current state

Last updated: 2026-10-17 (Africa/Johannesburg).

## Objective and boundary

Provide a clean, focused workflow for analyzing and forecasting from company presentations and reports without feeding the entire PDF to an LLM at once:
1. Scan the PDF locally for major sections (`section_capture/report_map.py`) so the LLM has an outline of the report.
2. Capture sections interactively using the PySide6 desktop app (`app.py` / `section_capture/`), exporting cropped PNG images and native text alongside a ready-to-paste Markdown prompt (`captures/`).
3. Prompt the LLM (`prompts/mining/00-report-orientation/v1.0.0` + `prompts/mining/12-analyst-reading-brief/v1.1.0`) to summarize important points, question consequential claims, and advise how to verify them in upcoming sections (`Pending: [section]`).

## Completed

- **Cleaned repository to core functionality only**:
  - Removed legacy whole-PDF page-inventory prompts/schemas (`01-page-inventory`), JSON fact-extraction prompts/schemas (`11-selected-section`), superseded v1.0.0 reading prompt, old evaluation/run folders (`runs/`, `evaluations/`, `templates/`), obsolete research/design docs, `prepared_prompts/`, `section_capture/prepare_prompt.py`, and temporary test directories.
  - Upgraded the existing 11-selection capture pack (`captures/20261017-115429-KEY-F26-FEATURES-7f02fcb4` and its `.zip`) in-place to the current `section_reading_package_v1` format with the embedded PAN FY2026 report map and `12-analyst-reading-brief/v1.1.0` prompt.
  - Streamlined `README.md`, `AGENTS.md`, `prompts/README.md`, `docs/CAPTURE_APP.md`, `docs/REPORT_MAP.md`, `docs/READING_BRIEF_WORKFLOW.md`, and `workflow/WORKFLOW.md`.
- **Verified test suite**:
  - Ran `.venv/Scripts/python.exe -m pytest tests -q -p no:cacheprovider --basetemp=tmp/pytest-clean` across all 26 unit and offscreen GUI tests covering PDF rendering, left/right panel isolation, native text & area capture, content types, native major-section scanning, report map caching/validation, and section package export.

## Next steps

1. Use `captures/20261017-115429-KEY-F26-FEATURES-7f02fcb4/` (or capture new sections via `Run Capture.cmd`) to run section-by-section analysis in your LLM chat.
2. Follow the `Pending: [section]` verification pointers in the LLM's response to capture the next relevant sections (CEO commentary, primary financial statements, financial notes, APMs, and operating/production tables) before building a forecast.
