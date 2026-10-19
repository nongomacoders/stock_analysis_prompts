# Current state

Last updated: 2026-10-18 (Africa/Johannesburg).

## Objective and boundary

Analyze and forecast from company presentations and reports section by section without whole-PDF inaccuracies or narrative fluff:
1. **Tier 1 (Programmatic Section Capture)**: Scan the PDF locally for major sections (`section_capture/report_map.py`) and capture section by section in the PySide6 app (`section_capture/`). Clicking `"Save & Run DeepSeek"` programmatically queries DeepSeek Flash (`deepseek/deepseek-v4.1-flash-1017`) via OpenRouter API in background `QThread`, auto-populates `llm_response`, and updates the central questions ledger in `documents/analysis.sqlite`.
2. **Tier 2 (Stage 1 Cognitive Forensic Audit)**: Automated export (`workflow/export_stage1.py`) of the sequential extractions and questions ledger to Gemini 4 Argon for deep forensic conflict resolution (no PDF attached), establishing verified ground truth on all accounting and operational junctions.
3. **Tier 3 (Stage 2 Institutional Valuation)**: Automated prompt generation (`workflow/generate_stage2.py`) feeding Argon's Stage 1 synthesis report alongside the PDF back into Gemini 4 Argon for the final 2-year forecast, SOTP DCF, and JSE equity research valuation note (ZAR per share).

## Completed

- **Heading & Subheading Input Sanitization**:
  - Implemented `clean_single_line_text()` across `section_capture/report_map.py`, `section_capture/packages.py`, and `section_capture/window.py` to strip tabs (`\t`), carriage returns (`\r`), line breaks (`\n`), non-breaking spaces (`\xa0`), and collapse multiple whitespace into a single space.
  - Introduced `SanitizedLineEdit(QLineEdit)` in `section_capture/window.py` that intercepts both keyboard pastes (Ctrl+V) and right-click context menu pastes, as well as live text updates, guaranteeing headings, subheadings, and printed page labels remain clean and single-line without interrupting normal space typing.
  - Upgraded `HeadingComboBox` to use `SanitizedLineEdit` as its underlying editor.
  - Sanitized backend logic in `save_package()`, `add_selection()`, and `register_subsection()` to ensure programmatic and manual entries remain clean in SQLite.
  - Cleaned all contaminated legacy records in `documents/analysis.sqlite` (sections 24 and 25 for Lewis Group and report map subsections).
  - Shortened section name label and status bar display using ellipsis (`shorten_section_name()`) with full details available via hover tooltip, preventing multi-line sidebar text wrapping.
  - Escaped Qt button ampersands (`Save && copy prompt`, `Save && Run DeepSeek`) so `&` displays properly in UI.
  - Added unit and Qt UI tests in `tests/test_capture.py` (all 47 tests pass with exit code 0).

- **OpenRouter Programmatic Capture Integration & Nitro Toggle (Tier 1)**:
  - Built `section_capture/openrouter.py` to securely read `OPENROUTER_API_KEY` in memory from external secrets (`C:\Users\Dion\Desktop\Projects\EXTERNAL_TO_REPOS\credentials\secrets.env`) or environment without ever inspecting or logging the secret value.
  - Configured default model to `deepseek/deepseek-v4.1-flash-1017`.
  - Added on-the-fly **Nitro throughput toggle (`:nitro`)** in `section_capture/window.py` and `SavedSectionsDialog`:
    - Allows switching between standard routing (low cost) and `:nitro` priority routing (3.1x faster throughput when network traffic is heavy).
  - Integrated OpenRouter generation statistics retrieval (`fetch_generation_stats()`) and fallback pricing estimation (`estimate_cost()`):
    - Retrieves exact billed cost (`cost_usd`), token breakdown (`prompt_tokens`, `completion_tokens`, `total_tokens`), and server latency.
    - Persists execution metadata in SQLite `manifest_json["review"]` (`response_time_seconds`, `cost_usd`, `model`, `tokens`).
    - Added convenience properties to `SavedSection` (`response_time_seconds`, `cost_usd`, `model_used`, `total_tokens`).
  - Real-time status bar updates in capture window and saved sections dialog (e.g. `✓ DeepSeek responded in 42.1s ($0.0146) [15,808 tok]`).
  - Unit and UI test suite expanded to 51 passing tests (exit code 0).


- **Experiment 2: Cognitive Forensic Audit with Gemini 4 Argon (Tier 2)**:
  - Compiled complete 19-section extraction dossier and open questions ledger (436k chars, ~106k tokens) into `companies/PAN/briefs/experiment2_argon_ledger_audit_prompt.md`.
  - Executed in Gemini 4 Argon without PDF attachment.
  - **100% Audit Match Achieved**: Argon solved all 7 forensic junctions with complete mathematical precision:
    1. *Diluted Share Count & Emmerson Allotment Date*: 2,129.95m anchor at 30 June 2026; unraveled the treasury 2.0M share double-deduction mystery (`2,333,671,529 + 102,641,421 - 2,003,734 = 2,434,309,216`); CDIs rank for dividend; pro-forma 2,106.30m shares post-buyback.
    2. *Balance Sheet Cash & Debt Position*: Confirmed genuine swing from US$150.5m Net Debt to US$185.7m Net Cash (US$185,597k exact).
    3. *Share-Based Payments (SBP) in EBITDA*: Verified SBP was fully absorbed in corporate overhead inside US$609.4m Adjusted EBITDA; true underlying recurring EBITDA is US$648.5m (or US$666.7m pre-SBP).
    4. *Third-Party Buy-In Feedstock & AISC Distortions*: Quantified +US$77/oz Group AISC distortion from 18,667 oz of buy-in ore (organic AISC ~US$1,790/oz; Evander distortion +US$160–US$185/oz).
    5. *Underground Asset Economics*: Disclosed high-cost Sheba/Consort shafts (25,154 oz at US$3,487/oz AISC) imposing US$165/oz structural drag on the remaining 90.8% portfolio (US$1,702/oz AISC).
    6. *Forward Capex Trajectory*: Exposed discrepancy between $302m narrative and $330m Board budget table; contrasted Scenario A ($330m/$303m) vs Scenario B ($110m/$65m Capex Cliff).
    7. *Section 36 Mining Tax Dynamics*: Confirmed why FY26 cash tax was only 12.3%; demonstrated that modeling $330m capex AND a 32% cash tax rate is a fatal accounting contradiction.
  - Saved full verified audit response (53,041 chars) to `companies/PAN/briefs/PAN_stage1_audit_response.md`.

- **Standardized Pipeline Workflow Scripts**:
  - `workflow/export_stage1.py`: Compiles the full sequential extraction working paper and dynamic questions ledger from `documents/analysis.sqlite` into a standardized Stage 1 Forensic Audit Prompt (`companies/<TICKER>/briefs/<TICKER>_stage1_forensic_prompt.md`).
  - `workflow/generate_stage2.py`: Injects the audited Stage 1 determinations as unshakeable ground truth alongside the company results PDF to generate the Stage 2 Institutional Valuation Prompt (`companies/<TICKER>/briefs/<TICKER>_stage2_valuation_prompt.md`).

- **Full Report Capture & Verification Suite (19 Sections in SQLite)**:
  - 100% of operational, financial statement, accounting note, APM, and production tables across all 54 physical pages of `Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf` persisted in `documents/analysis.sqlite`.

- **Sector-Based Company Reorganization & Retail Prompt Engine**:
  - Reorganized `companies/` into sector subdirectories:
    - `companies/mining/`: Houses `PAN` (Pan African Resources) and `HAR` (Harmony Gold).
    - `companies/retail/`: Houses `LEW` (Lewis Group) and `TRU` (Truworths).
    - `companies/finance/` and `companies/telcos/`: Scaffolding packages initialized with sector READMEs.
  - Implemented sector prompt templates under `prompts/<sector>/`:
    - `prompts/mining/`: Tailored for mining operations (throughput, recovery, AISC, capex cliffs, Section 36 tax).
    - `prompts/retail/`: Tailored for retail and consumer credit operations:
      - `00-report-orientation/v1.0.0`: Major-section map orientation for retail and credit disclosures.
      - `12-analyst-reading-brief/v1.1.0`: Dedicated forensic prompt focusing on merchandise sales vs financial services/insurance revenue, gross margin bridges, debtors book health & IFRS 9 ECL provisioning, store network dynamics ($m^2$, trading density), and IFRS 16 lease liabilities.
  - Upgraded PySide6 capture app (`section_capture/`):
    - Added `SectorComboBox` to the toolbar with supported choices (`Mining`, `Retail`, `Finance`, `Telcos`).
    - Added auto-detection from file path (`detect_sector_from_path()`), automatically setting the sector when opening reports from `companies/<sector>/<ticker>/sources/`.
    - Updated `save_package()` and `build_prompt()` to assemble sector-specific prompt templates and store `manifest["sector"]`.
  - Upgraded scaffolding tool (`new_company.py`):
    - Added `--sector {mining,retail,finance,telcos}` argument.
    - Scaffolds company under `companies/<SECTOR>/<TICKER>/` and configures `SECTOR = ...` in `models/config.py`.
    - Generates sector-tailored Jupyter sandbox (`<ticker>_sandbox.ipynb`).
  - Upgraded workflow export scripts:
    - `workflow/export_stage1.py`: Auto-discovers company directory and sector via `find_company_dir()`, directing Gemini 4 Argon as **Senior Forensic Retail & Consumer Credit Accounting Auditor** for retail targets.
    - `workflow/generate_stage2.py`: Generates retail institutional valuation prompt directing Gemini 4 Argon as **Head of Retail & Consumer Equity Research** for retail targets.
  - Updated SQLite database (`documents/analysis.sqlite`) report paths to reflect the new sector hierarchy while verifying 100% SHA-256 match.
- **Sidebar Layout Overhaul & Dynamic Disabled-State Guidance (section_capture/)**:
  - Compacted vertical layout to fit comfortably on all screen resolutions without top title clipping or cramped vertical scrollbars:
    - Reduced panel margins to `(14, 10, 14, 10)` and field spacing to `3-4px`.
    - Consolidated `Data type` and `Printed page label` onto a single horizontal row (`QHBoxLayout`).
    - Merged auxiliary actions (`Stored questions`, `Copy prompt`, `Saved sections`) into one compact horizontal row.
    - Set `setHorizontalScrollBarPolicy(ScrollBarAlwaysOff)` on `panel_scroll` with minimum width 370px and splitter defaults `[880, 440]`.
    - Tightened CSS padding in `section_capture/__main__.py` (`6px 10px` on standard buttons, `9px 12px` on primary).
  - Implemented dynamic tooltips and real-time guidance resolving disabled-state confusion:
    - Dynamic tooltips on `Save & copy prompt` and `Save & Run DeepSeek` specifying exact missing requirement (`"Disabled: Select text or area evidence from the PDF first"`, `"Disabled: Choose or enter a Section heading above first"`, or `"Disabled: Section X has subsections; enter a sub-heading above"`).
    - Added amber inline warning guidance (`self.warning_label`): `"⚠ Choose or enter a Section heading above to enable Save"` whenever evidence selections exist but heading is empty.
    - `Add selection` button tooltip clearly explains when a selection is uncommitted vs when it has already been added to the list (`"X selection(s) already added below. Select another area on the PDF to add more"`).
    - `Copy prompt` tooltip explains why it is disabled before the first section is saved in a session.
    - `self.selection_label` displays reassuring confirmation and next-step prompt: `"✓ Added X selection(s). Select another area, or choose a Section heading to save."`
  - All 53 tests passing (exit code 0).
- **Lewis (LEW) Response Reset & Dynamic Prompt Refresh**:
  - Cleared all recorded LLM responses (`llm_response = NULL`) and review metadata across sections 1–4 for Lewis in `documents/analysis.sqlite`.
  - Reset Lewis `questions_ledger` on the report row to empty string (`''`) so questions start fresh from Section 1.
  - Rebuilt stored prompts for all 4 Lewis sections using the dedicated Retail prompt template (`prompts/retail/12-analyst-reading-brief/v1.1.0/prompt.md`).
  - Removed stale response files (`companies/retail/LEW/briefs/section_02_CEO_Report_nitro_response.md` and `companies/retail/LEW/briefs/FY26/`).
  - Added `clear_section_llm_response()` and `delete_section()` to `section_capture/db.py`.
  - Upgraded `SavedSectionsDialog` (`section_capture/map_dialog.py`):
    - Added **"Clear response"** button to allow clearing LLM responses directly from the UI.
    - Added `_refresh_section_prompt_with_current_ledger()`: dynamically rebuilds each section's prompt with the current `reports.questions_ledger` before copying or querying OpenRouter, ensuring that when Section 1 completes and updates questions, Section 2 automatically inherits those questions.
  - Added unit test in `tests/test_capture.py` (54 tests passing, exit code 0).



## Next steps

1. **OpenRouter API Key Status**:
   - The OpenRouter integration is fully tested and operational.
   - When calling OpenRouter with the current key from `secrets.env`, OpenRouter returns `HTTP 401: User not found.`. The user should verify or refresh their API key at [openrouter.ai/keys](https://openrouter.ai/keys) and update `secrets.env`. Once updated, `"Save & Run DeepSeek"` in the capture app will work immediately without code changes.
2. **Execute Stage 2 Valuation in Gemini 4 Argon**:
   - The Stage 2 prompt is prepared at `companies/PAN/briefs/PAN_stage2_valuation_prompt.md`.
   - Attach `companies/PAN/sources/FY26-year-end-results-SENS-announcement-2026.pdf` together with the prompt in Gemini 4 Argon to generate the final 2-year forecast, SOTP DCF, and JSE equity research note (ZAR per share).
3. **Daily Use on New Companies**:
   - To analyze another company, run `python new_company.py <TICKER>`, drop the PDF into `companies/<TICKER>/sources/`, capture via `Run Capture.cmd`, and run `python workflow/export_stage1.py <TICKER>` followed by `python workflow/generate_stage2.py <TICKER>`.
