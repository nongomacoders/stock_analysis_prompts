# Report Section Capture App

Local PySide6 desktop app (`v0.4.0`) that scans a company PDF report into major sections, lets you select text or area crops across pages, and exports a ready-to-paste LLM reading prompt alongside cropped PNG evidence.

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

## Capturing a section

1. **Open PDF**: Loads a cached major-section map from `documents/maps/<sha256>/` or scans native PDF headings automatically. Use **Report map → Copy overview** to orient your LLM chat.
2. **Navigate & select**:
   - Move through physical PDF pages (`1`-based).
   - Choose **Area selection** to draw a rectangle around tables, charts, or panels, or **Text selection** to highlight prose.
   - Use `+` / `−`, `Ctrl+Wheel`, or **Fit page** to adjust zoom.
3. **Tag & add**:
   - Choose the **Data type** (`Commentary`, `Table`, `Financial note`, or `Mixed / unspecified`) and optional **Printed page label**.
   - Click **Add selection to section** to combine multiple crops/pages into one section pack. You can retag any added item using **Set type**.
4. **Save & upload**:
   - Enter a **Section heading** (and optional **Analyst question**) and click **Save section + upload ZIP**.
   - Click **Open saved folder** to attach `evidence/S001.png`, `S002.png`, etc. to your LLM chat, and click **Copy reading prompt** to paste `prompt.md`.

## Saved package layout

```text
captures/<timestamp-heading-id>/
  manifest.json          Source PDF SHA-256, physical pages, coordinates, and data types
  prompt.md              Complete prompt with report map, instructions, and extracted text
  report-overview.md     Standalone major-section outline
  report-map.json        Source-bound section map snapshot
  selected-text.txt      Combined native text for quick review
  UPLOAD.md              Upload instructions
  evidence/S001.png      Cropped high-DPI image of selection 1
  evidence/S001.txt      Native text extracted from selection 1
captures/<timestamp-heading-id>.zip
```

## Running tests

```powershell
.venv\Scripts\python.exe -m pytest tests -q -p no:cacheprovider --basetemp=tmp/pytest
```
