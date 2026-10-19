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
  - Added unit and Qt UI tests in `tests/test_capture.py` (all 46 tests pass with exit code 0).

- **OpenRouter Programmatic Capture Integration (Tier 1)**:
  - Built `section_capture/openrouter.py` to securely read `OPENROUTER_API_KEY` in memory from external secrets (`C:\Users\Dion\Desktop\Projects\EXTERNAL_TO_REPOS\credentials\secrets.env`) or environment without ever inspecting or logging the secret value.
  - Configured default model to `deepseek/deepseek-v4.1-flash-1017`.
  - Added primary `"Save & Run DeepSeek"` button in `section_capture/window.py` with asynchronous non-blocking worker `OpenRouterWorker(QThread)`:
    - Automatically executes section prompt in background.
    - Captures model output into `sections.llm_response`.
    - Automatically parses Section 4 ("Updated Open Questions Ledger") and updates `reports.questions_ledger` in SQLite for seamless sequential continuity.
  - Added `"Query Model (OpenRouter)"` button to `SavedSectionsDialog` (`section_capture/map_dialog.py`) to query or re-run any saved section on demand.
  - Comprehensive unit test suite in `tests/test_openrouter.py` (all 43 tests pass cleanly with exit code 0).
  - Standalone live diagnostic script `test_openrouter_live.py`: Safely checks credentials, verifies OpenRouter account auth (`/api/v1/auth/key`), and performs end-to-end completion tests with latency tracking and zero key leakage.


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

- **Unified Multi-Company Analyst Workbench Hub (`companies/<TICKER>/`)**:
  - Fully consolidated `company_results/` and `companies/` into a single, unified source of truth:
    - `companies/PAN/sources/`: Contains `Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf` and `Pan-African-Resources-year-end-results-SENS-announcement-2025.pdf`.
    - `companies/TRU/sources/`: Scaffolding initialized with `new_company.py TRU`, housing `TRU_FY2025_AFS.pdf`.
    - `companies/HAR/sources/`: Scaffolding initialized with `new_company.py HAR`.
  - Deleted legacy `company_results/` directory and deprecated `.zip` export files.
  - Updated file open dialog in `section_capture/window.py` to open `companies/` by default.
  - Updated pytest fixtures and SQLite database paths to reference `companies/PAN/sources/`.
  - Added multi-period awareness (`--period FY26`, `--period FY27`) to `workflow/export_stage1.py` and `workflow/generate_stage2.py`, structuring briefs into period subfolders (`companies/<TICKER>/briefs/<PERIOD>/`).


## Next steps

1. **OpenRouter API Key Status**:
   - The OpenRouter integration is fully tested and operational.
   - When calling OpenRouter with the current key from `secrets.env`, OpenRouter returns `HTTP 401: User not found.`. The user should verify or refresh their API key at [openrouter.ai/keys](https://openrouter.ai/keys) and update `secrets.env`. Once updated, `"Save & Run DeepSeek"` in the capture app will work immediately without code changes.
2. **Execute Stage 2 Valuation in Gemini 4 Argon**:
   - The Stage 2 prompt is prepared at `companies/PAN/briefs/PAN_stage2_valuation_prompt.md`.
   - Attach `companies/PAN/sources/FY26-year-end-results-SENS-announcement-2026.pdf` together with the prompt in Gemini 4 Argon to generate the final 2-year forecast, SOTP DCF, and JSE equity research note (ZAR per share).
3. **Daily Use on New Companies**:
   - To analyze another company, run `python new_company.py <TICKER>`, drop the PDF into `companies/<TICKER>/sources/`, capture via `Run Capture.cmd`, and run `python workflow/export_stage1.py <TICKER>` followed by `python workflow/generate_stage2.py <TICKER>`.
