# Current state

Last updated: 2026-10-17 (Africa/Johannesburg).

## Objective and boundary

Provide a clean, focused workflow for analyzing and forecasting from company presentations and reports without feeding the entire PDF to an LLM at once:
1. Scan the PDF locally for major sections (`section_capture/report_map.py`) so the LLM has an outline of the report.
2. Capture sections interactively using the PySide6 desktop app (`app.py` / `section_capture/`), exporting cropped PNG images and native text alongside a ready-to-paste Markdown prompt (`captures/`).
3. Prompt the LLM (`prompts/mining/00-report-orientation/v1.0.0` + `prompts/mining/12-analyst-reading-brief/v1.1.0`) to summarize important points, question consequential claims, and advise how to verify them in upcoming sections (`Pending: [section]`).

## Completed

- **Cleaned repository to core functionality and reset for a fresh PAN capture**:
  - Removed all previous PAN captures and generated prompts (`captures/`), cached PAN section maps and document registry (`documents/`), legacy prompts/schemas (`01-page-inventory`, `11-selected-section`, `12-analyst-reading-brief/v1.0.0`), old evaluation/run folders (`runs/`, `evaluations/`, `templates/`, `prepared_prompts/`), obsolete design docs, and temporary directories.
  - Isolated the test suite's map cache in a temporary directory (`tests/conftest.py`) so running tests never creates or relies on pre-baked map files in `documents/`.
  - Verified all 26 automated unit and offscreen GUI tests pass (`EXIT_CODE=0`).

## Next steps

1. Launch the app via `Run Capture.cmd` and open `company_results/PAN/FY-2026/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf` to start a completely fresh section scan and capture session.
2. Follow the `Pending: [section]` verification pointers in the LLM's response as you capture and feed each section sequentially.
