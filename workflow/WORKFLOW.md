# Working process

## Core workflow

1. **Scan major sections first**: Opening a PDF in the local PySide6 app (`app.py`) scans native headings across all physical pages (`section_capture/report_map.py`) to build a coarse major-section map (`documents/maps/<sha256>/`).
2. **Capture in sections**: Select text or area regions from the PDF (`section_capture/pdf_source.py`, `section_capture/window.py`), assign an explicit data type (`commentary`, `table`, `financial_note`, or `unspecified`), and save an immutable section pack (`section_capture/packages.py`).
3. **Note key points & advise verification in upcoming sections**: Each saved pack combines `prompts/mining/00-report-orientation/v1.0.0/prompt.md` and `prompts/mining/12-analyst-reading-brief/v1.1.0/prompt.md` with the report map and selected evidence. The LLM summarizes key points, questions consequential claims, and marks cross-section checks as `Pending: [section]` for upcoming sections.

## Evidence integrity rules

- Original PDFs in `company_results/` remain read-only; source SHA-256 is verified before every save.
- Physical PDF pages are numbered from 1; printed page labels are stored only when explicitly entered by the user.
- Area selections extract only characters fully inside the crop box and warn when boundaries cross text or when a region is image-only.
- Report map availability shows what other sections exist for later reading; it does not imply those sections have already been inspected or verified.
