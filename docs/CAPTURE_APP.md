# Report Section Capture App

Local PySide6 desktop app (`v0.4.0`) that scans a company PDF report into major sections, stores running verification questions across sections, lets you select text or area crops across pages, and saves all extracted text, prompts, LLM responses, and question ledgers in a single SQLite database (`documents/analysis.sqlite`).

## Running the app

Double-click **`Run Capture.cmd`**, or run from the project root:

```powershell
.venv\Scripts\python.exe app.py
```

To open a specific PDF directly:

```powershell
.venv\Scripts\python.exe app.py "companies\PAN\sources\Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf"
```


On another machine, install `uv` and run `./setup.ps1` to create `.venv` from `requirements.lock.txt`.

## Scaffolding & Ticker Examination Hub

The app includes a **New Company Hub** dialog to initialize new company hubs without leaving the GUI:
1. Enter any JSE ticker symbol (e.g. `DCP`, `VOD`, `RBX`, `PIK`).
2. Click **🔍 Examine Ticker**: The system queries local registries, fetches verified JSE profile data via Yahoo Finance (`<TICKER>.JO`), and queries OpenRouter with live web search (`plugins: [{"id": "web"}]`) to verify the authentic JSE listing and check Stage 1 / Stage 2 prompt readiness.
3. Automatically populates legal company name, sector code, and audit preview card.
4. Optionally drop or browse for an initial PDF report to automatically copy into `sources/` and open in the capture app.

## Progressive section workflow

1. **Open PDF**: Loads the report's major-section map and open verification questions from `documents/analysis.sqlite` (or scans native PDF headings automatically on first open).
2. **Navigate & select**:
   - Move through physical PDF pages (`1`-based).
   - Choose **Area selection** to draw a rectangle around tables, charts, or panels (tables are automatically formatted as pipe-separated Markdown tables with `[^1]` superscript footnotes), or **Text selection** to highlight prose.
   - Edit the extracted text directly in the preview box if needed.
3. **Tag & add**:
   - Choose the **Data type** (`Commentary`, `Table`, `Financial note`, or `Mixed / unspecified`) and optional **Printed page label**.
   - Click **Add selection to section** to combine multiple crops/pages into one section capture.
4. **Save & prompt the LLM**:
   - Choose or enter a **Section heading** (and optional **Sub-heading** to divide large sections into numbered subsections like `D005.1`, `D006.1`).Once a section has subsections, a sub-heading is required for subsequent captures under that heading.
   - Click **Save section & copy prompt**. The app stores the section in `documents/analysis.sqlite` and automatically copies the complete reading prompt to your clipboard.
5. **Store LLM response & update open questions**:
   - Click **Saved sections / LLM response** (or **Stored questions**) to paste the LLM's Markdown response.
   - Saving the LLM response stores it on that section row in SQLite and automatically extracts Section 4 (`Updated Open Questions Ledger`) into the report's `questions_ledger` for the next section capture.

## SQLite schema (`documents/analysis.sqlite`)

- **`reports`**: `sha256` (PK), `filename`, `original_path`, `byte_size`, `physical_page_count`, `report_map_json`, `questions_ledger`, `created_at`, `updated_at`
- **`sections`**: `id` (PK), `package_id` (UNIQUE), `report_sha256` (FK), `section_number`, `section_id`, `heading`, `subheading`, `analyst_question`, `selected_text`, `selections_json`, `stored_questions_snapshot`, `prompt`, `llm_response`, `manifest_json`, `created_at`, `updated_at`

## Running tests

```powershell
.venv\Scripts\python.exe -m pytest tests -q -p no:cacheprovider --basetemp=tmp/pytest
```

