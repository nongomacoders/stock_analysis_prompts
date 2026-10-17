# Report Section Capture App

Local PySide6 desktop app (`v0.4.0`) that scans a company PDF report into major sections, stores running verification questions across sections, lets you select text or area crops across pages, and exports a ready-to-paste LLM prompt alongside cropped PNG evidence.

## Running the app

Double-click **`Run Capture.cmd`**, or run from the project root:

```powershell
.venv\Scripts\python.exe app.py
```

To open a specific PDF directly:

```powershell
.venv\Scripts\python.exe app.py "company_results\PAN\FY-2026\Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf"
```

On another machine, install `uv` and run `./setup.ps1` to create `.venv` from `requirements.lock.txt`.

## Progressive section workflow

1. **Open PDF**: Loads a cached major-section map from `documents/maps/<sha256>/` (or scans native PDF headings automatically) and loads any stored verification questions for that PDF from `documents/questions/<sha256>/questions-ledger.md`.
2. **Navigate & select**:
   - Move through physical PDF pages (`1`-based).
   - Choose **Area selection** to draw a rectangle around tables, charts, or panels (tables are automatically formatted as pipe-separated Markdown tables with `[^1]` superscript footnotes), or **Text selection** to highlight prose.
   - Edit the extracted text directly in the preview box if needed.
3. **Tag & add**:
   - Choose the **Data type** (`Commentary`, `Table`, `Financial note`, or `Mixed / unspecified`) and optional **Printed page label**.
   - Click **Add selection to section** to combine multiple crops/pages into one section pack.
4. **Save & prompt the LLM**:
   - Enter a **Section heading** and click **Save section + upload ZIP**.
   - Click **Open saved folder** to attach `evidence/S001.png`, `S002.png`, etc. to your LLM chat, and click **Copy reading prompt** to paste `prompt.md`.
   - `prompt.md` automatically embeds the report section map and your **Stored questions** from earlier sections.
5. **Store updated questions for the next section**:
   - Copy the **Updated Open Questions Ledger** block from the LLM's response.
   - Click **Stored questions** (in the toolbar or sidebar) and click **Replace from clipboard & Save**.
   - When you capture the next section, those updated questions are automatically included in the next `prompt.md`.

## Saved package layout

```text
<save-folder>/<timestamp-heading-id>/
  manifest.json          Source PDF SHA-256, physical pages, coordinates, data types, and stored questions
  prompt.md              Complete prompt with report map, stored questions, instructions, and extracted text
  report-overview.md     Standalone major-section outline
  report-map.json        Source-bound section map snapshot
  stored-questions.md    Snapshot of stored questions supplied with this section (when present)
  selected-text.txt      Combined native text for quick review
  UPLOAD.md              Upload instructions
  evidence/S001.png      Cropped high-DPI image of selection 1
  evidence/S001.txt      Structured text / Markdown table extracted from selection 1
<save-folder>/<timestamp-heading-id>.zip
```

## Running tests

```powershell
.venv\Scripts\python.exe -m pytest tests -q -p no:cacheprovider --basetemp=tmp/pytest
```
