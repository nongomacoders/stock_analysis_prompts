# Company Report Section Capture & Reading Brief

Scan a company PDF report into major sections, capture selected sections as visual + native-text evidence packs, and prompt an LLM to summarize the important points and advise how to verify claims in upcoming sections.

## Quick start

Double-click **`Run Capture.cmd`**, or run:

```powershell
.venv\Scripts\python.exe app.py
```

On a fresh checkout, run `./setup.ps1` first to create the local Python 3.12 `.venv` via `uv`.

## Workflow

1. **Open PDF**: The app automatically scans native titles and running headings across all physical pages to build a coarse major-section map (cached in `documents/maps/<sha256>/`).
2. **Orient the chat (optional)**: Click **Report map → Copy overview** to paste the report outline into your LLM chat before sending the first section.
3. **Capture a section**:
   - Enter a **Section heading** and optional **Analyst question**.
   - Select regions using **Area selection** (tables, charts, multi-column boxes) or **Text selection** (prose).
   - Tag each selection's **Data type** (`Commentary`, `Table`, `Financial note`, or `Mixed / unspecified`) and click **Add selection to section**.
   - Click **Save section + upload ZIP**.
4. **Prompt the LLM**:
   - Click **Open saved folder** and upload the cropped PNGs from `evidence/` into your LLM chat.
   - Click **Copy reading prompt** and paste it into the chat.
   - The prompt includes the report section map (marking which sections have partial evidence in this upload vs. which are still upcoming) and instructs the LLM to note key points, question consequential claims, and mark cross-section checks as `Pending: [section]` for upcoming sections.

## Project structure

```text
app.py                                    Application entry point
Run Capture.cmd                           Windows launcher
setup.ps1                                 Environment setup script (uv)
section_capture/                          PySide6 PDF section scanner, canvas, and pack exporter
prompts/mining/00-report-orientation/     Report map orientation prompt (v1.0.0)
prompts/mining/12-analyst-reading-brief/  Section analysis & upcoming-verification prompt (v1.1.0)
company_results/<ticker>/<period>/        Original PDF reports
documents/                                Source document registry and cached section maps
captures/                                 Local saved section packs and upload ZIPs (Git-ignored)
docs/                                     App, report map, and reading workflow guides
tests/                                    Automated offscreen Qt, crop, map, and export tests
workflow/                                 Project state and workflow notes
```

See [docs/CAPTURE_APP.md](docs/CAPTURE_APP.md), [docs/REPORT_MAP.md](docs/REPORT_MAP.md), and [docs/READING_BRIEF_WORKFLOW.md](docs/READING_BRIEF_WORKFLOW.md) for details.
