# Company Report Section Capture & Reading Brief

Scan a company PDF report into major sections, capture selected sections as visual + native-text evidence packs, and prompt an LLM to summarize the important points and advise how to verify claims in upcoming sections.

## Current project summary

The aim is to make DeepSeek's report analysis more reliable through better evidence,
manageable sections, focused prompts and an evolving ledger of questions. The local
PySide6 app maps report headings, captures native text and page images, and preserves
source filenames, SHA-256 hashes and physical PDF page numbers.

- **Read and question:** DeepSeek analyzes captured sections using a shared reading
  task and conditional sector notes. Relevant unresolved questions carry forward;
  structured updates require evidence from the current capture. Oversized captures
  are split without silently dropping remaining pages.
- **Synthesize and evaluate:** DeepSeek performs Stage 1 and Stage 2 analysis.
  Material unresolved valuation dependencies require withholding the target and
  recommendation. A successful API call or valid ledger is not financial validation.
- **Review and improve:** the user runs Gemini reviews in Antigravity; Codex checks
  those reviews against original evidence. Additional GLM/OpenCode comparisons are
  preserved as independent, reviewable claims. Verified lessons inform prompt and
  question improvements; raw model outputs and earlier valuations remain preserved.

DeepSeek requests currently use Fireworks through OpenRouter, with provider fallback
disabled. Experiment records retain request settings, generation identifiers, tokens,
cost and timing. Credentials are loaded externally and excluded from those records.

Recent work improves table/prose extraction, portfolio sign guidance, disjoint
aggregation and question-closure instructions. Small NTU/PAN experiments found that
three separate meaning/calculation/explanation calls improve presentation but have
not demonstrated sufficient reliability to replace the current single-call section
workflow. Scope errors and premature closures remain known limitations.

See [workflow/STATE.md](workflow/STATE.md) for current results and next work,
[docs/SECTION_READING_PROMPT.md](docs/SECTION_READING_PROMPT.md) for prompt assembly,
and [docs/VALUATION_WITHHOLDING.md](docs/VALUATION_WITHHOLDING.md) for publication checks.

## Quick start

Double-click **`Run Capture.cmd`**, or run:

```powershell
.venv\Scripts\python.exe app.py
```

On a fresh checkout, run `./setup.ps1` first to create the local Python 3.12 `.venv` via `uv`.

## Workflow

1. **Open PDF**: The app automatically scans native titles and running headings across all physical pages to build a coarse major-section map (cached locally under `documents/maps/<sha256>/`).
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
prompts/mining/00-report-orientation/     Report map orientation prompt template (v1.0.0)
prompts/mining/12-analyst-reading-brief/  Section analysis & upcoming-verification prompt template (v1.1.0)
companies/<sector>/<ticker>/                Company sources, briefs, models, research and evaluation records
ARCHITECTURE.md                           Comprehensive technical specification and pipeline architecture
docs/                                     App, report map, and reading workflow guides
tests/                                    Automated offscreen Qt, crop, map, and export tests
workflow/                                 Project state, workflow notes, and Stage 1/2 export scripts
```

See [ARCHITECTURE.md](ARCHITECTURE.md), [docs/CAPTURE_APP.md](docs/CAPTURE_APP.md), [docs/REPORT_MAP.md](docs/REPORT_MAP.md), and [docs/READING_BRIEF_WORKFLOW.md](docs/READING_BRIEF_WORKFLOW.md) for details.

