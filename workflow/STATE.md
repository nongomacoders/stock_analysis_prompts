# Current state

Last updated: 2026-10-17 (Africa/Johannesburg).

## Objective and boundary

Provide a clean, focused workflow for analyzing and forecasting from company presentations and reports without feeding the entire PDF to an LLM at once:
1. Scan the PDF locally for major sections (`section_capture/report_map.py`) so the LLM has an outline of the report.
2. Capture sections interactively using the PySide6 desktop app (`app.py` / `section_capture/`), exporting cropped PNG images and structured native text alongside a ready-to-paste Markdown prompt (`captures/`).
3. Prompt the LLM (`prompts/mining/00-report-orientation/v1.0.0` + `prompts/mining/12-analyst-reading-brief/v1.1.0`) to summarize important points, question consequential claims, and advise how to verify them in upcoming sections (`Pending: [section]`).

## Completed

- **Cleaned repository to core functionality and reset for a fresh PAN capture**:
  - Removed all previous PAN captures and generated prompts (`captures/`), cached PAN section maps and document registry (`documents/`), legacy prompts/schemas (`01-page-inventory`, `11-selected-section`, `12-analyst-reading-brief/v1.0.0`), old evaluation/run folders (`runs/`, `evaluations/`, `templates/`, `prepared_prompts/`), obsolete design docs, and temporary directories.
  - Isolated the test suite's map cache in a temporary directory (`tests/conftest.py`) so running tests never creates or relies on pre-baked map files in `documents/`.
- **Improved table & footnote extraction and added editable preview**:
  - Added `extract_structured_text` in `section_capture/pdf_source.py` to detect tabular column intervals from `pdfplumber` character coordinates, format tabular crops as pipe-separated Markdown tables (`| col1 | col2 | ... |`), merge stacked multi-line headers above horizontal rules, format smaller superscript footnote markers as `[^1]`, merge wrapped first-column labels, and keep titles/footnotes outside the table grid.
  - Made the extracted text preview in `section_capture/window.py` editable so pending or added selections can be tweaked before saving.
  - Added automated tests in `tests/test_capture.py` verifying Markdown table formatting, superscript footnotes, blank first-column sub-row alignment, and editable preview persistence (`28 passed`, `EXIT_CODE=0`).

## Next steps

1. Restart `Run Capture.cmd` and re-select your PAN sections—tables will now appear as clean Markdown tables in the editable preview box.
2. Follow the `Pending: [section]` verification pointers in the LLM's response as you capture and feed each section sequentially.
