# Current state

Last updated: 2026-10-18 (Africa/Johannesburg).

## Objective and boundary

Analyze and forecast from company presentations and reports section by section without whole-PDF inaccuracies or narrative fluff:
1. **Tier 1 (Programmatic Section Capture)**: Scan the PDF locally for major sections (`section_capture/report_map.py`) and capture section by section in the PySide6 app (`section_capture/`). Clicking `"Save & Run DeepSeek"` programmatically queries DeepSeek Flash (`deepseek/deepseek-v4.1-flash-1017`) via OpenRouter API in background `QThread`, auto-populates `llm_response`, and updates the central questions ledger in `documents/analysis.sqlite`.
2. **Tier 2 (Stage 1 Cognitive Forensic Audit)**: Automated export (`workflow/export_stage1.py`) of the sequential extractions and questions ledger to Gemini 4 Argon for deep forensic conflict resolution (no PDF attached), establishing verified ground truth on all accounting and operational junctions.
3. **Tier 3 (Stage 2 Institutional Valuation)**: Automated prompt generation (`workflow/generate_stage2.py`) feeding Argon's Stage 1 synthesis report alongside the PDF back into Gemini 4 Argon for the final 2-year forecast, SOTP DCF, and JSE equity research valuation note (ZAR per share).

## Completed

- **FTSE/JSE ICB Sector Codes & Classifications Integration**:
  - Integrated official FTSE/JSE Industry Classification Benchmark (ICB) sector codes, index codes, and sector names while preserving canonical directory slugs (`mining`, `retail`, `reit`, `it`, `construction`, `finance`, `telcos`):
    - Added `jse_code`, `icb_code`, and `jse_sector_name` to `SectorConfig` in `companies/sectors.py`:
      - `mining`: `JS5513` (Precious Metals and Mining / ICB `551030`) by default, with `JS5512` (Industrial Metals and Mining / ICB `551020`) override for `ORN` (Orion Minerals) and `AFT` (Afrimat).
      - `retail`: `JS4041` (Retailers / ICB `404010`).
      - `reit`: `JS3512` (Real Estate Investment Trusts / ICB `351020`).
      - `it`: `JS1011` (Software and Computer Services / ICB `101010`).
      - `construction`: `JS5011` (Construction and Materials / ICB `501010`).
      - `finance`: `JS3011` (Banks & Financial Services / ICB `301010`).
      - `telcos`: `JS1512` (Telecommunications Service Providers / ICB `151020`).
    - Added helper functions `get_jse_sector_code()`, `get_icb_code()`, `get_jse_sector_name()`, and `get_jse_sector_label()` (e.g. `"Mining (JS5513)"`, `"Retail (JS4041)"`).
    - Updated `resolve_sector_alias()` and `normalize_sector_code()` to recognize all FTSE/JSE index codes and ICB numeric codes.
    - Updated `new_sector.py` CLI to accept `--jse-code`, `--icb-code`, and `--jse-name`.
    - Updated `workflow/generate_stage2.py` to embed `jse_sector_code` and `jse_sector_name` into the mandatory Stage 2 JSON summary block and Markdown summary table.
    - Updated `section_capture/db.py` to extract `jse_sector_code` and `jse_sector_name` into `valuation_summary_json` and `get_analyzed_stocks()`.
    - Updated `section_capture/portfolio_view.py` and `section_capture/audit_dialog.py` to display JSE sector codes on badges, tables, and KPI banners.
    - Synced all 5 completed Stage 2 valuation markdown notes on disk (`PAN`, `LEW`, `ORN`, `APF`, `IOC`) and backfilled `documents/analysis.sqlite`.
    - Added unit and integration tests in `tests/test_sectors.py` and `tests/test_portfolio_valuation.py`. All 109 tests pass.

- **Stage 2 Institutional Valuation Sector Normalization & Construction Sector Support**:
  - Identified and fixed sector tracking in Stage 2 Institutional Valuation notes and database persistence:
    - Added `normalize_sector_code()` in `companies/sectors.py` to deterministically map raw sector strings, aliases, and Markdown table cell descriptions (e.g. `"Mining (Gold)"`, `"JSE Retail"`, `"REIT / Listed Property"`, `"Technology / IT Services"`) to canonical sector codes (`"mining"`, `"retail"`, `"reit"`, `"it"`, `"construction"`).
    - Updated `parse_valuation_summary()` in `section_capture/db.py` to extract `"sector"` from both the mandatory JSON summary block (`data.get("sector")`) and Section 1 summary tables / bullet points (`**Sector:** ...`), saving it into `valuation_summary_json`.
    - Added automatic sector fallback in `save_stage2_report()` using `detect_company_meta()` if the valuation note response omits the sector.
    - Added dedicated `construction` operating model and persona branch in `workflow/generate_stage2.py` (Head of Construction & Materials Equity Research, residential development pipeline units, serviced stands, memorial park plot margins, infrastructure contracting order book, DMTN bond covenants, and SOTP NAV).
    - Resolved `CGR` company title fallback to use `KNOWN_COMPANIES` (`"Calgro M3 Holdings"`) instead of `"CGR Resources"`.
    - Regenerated `companies/construction/CGR/briefs/FY26/CGR_FY26_stage2_valuation_prompt.md`.
    - Backfilled `reports.valuation_summary_json` in `documents/analysis.sqlite` for all 5 existing reports (`PAN`: mining, `LEW`: retail, `ORN`: mining, `APF`: reit, `IOC`: it).
    - Added unit test coverage in `tests/test_sectors.py` and `tests/test_portfolio_valuation.py`. All 108 tests pass.

- **Portable Relative Path & Immediate SHA-256 PDF Registration**:
  - Implemented `to_relative_project_path()` and `resolve_project_path()` in `section_capture/db.py`.
  - When opening any PDF in `CaptureWindow.open_pdf()`, the SHA-256 hash is computed immediately and the file path is normalized and stored as a portable forward-slash relative path (`companies/<sector>/<ticker>/sources/<filename>.pdf`) in `reports.original_path`.
  - Upgraded `discover_available_companies()` and `resolve_project_path()` to handle both relative and foreign absolute paths seamlessly across different developer machines and user account paths (e.g. `diond` vs `Dion`).
  - Migrated all existing records in `documents/analysis.sqlite` to clean canonical relative paths.

- **Stage 1 Forensic Audit Multi-Document & CGR Resolution**:
  - Resolved "No Sections Found" error when compiling Stage 1 Forensic Audit for Calgro M3 Holdings (`CGR`):
    - Added `"CGR": ("Calgro M3 Holdings", "construction")` and `"CALGRO"` alias to `KNOWN_COMPANIES` in `section_capture/db.py`.
    - Enhanced `detect_company_meta()` to match company name tokens (e.g. `calgro` in `10023_Calgro-IR-2026_WEB-FA3.pdf`).
    - Fixed company resolution precedence in `get_analyzed_stocks()` to prefer `r["original_path"]` over `r["filename"]`, correctly utilizing directory structure `companies/<sector>/<ticker>/sources/` rather than guessing from standalone filenames.
    - Updated `discover_available_companies()` and `AuditValuationDialog._apply_company_data()` to query SQLite for existing PDF report records (`sha256` and section count) rather than leaving discovered company directories in a generic `Scaffolded` state with blank SHA-256.
    - Upgraded `AuditValuationDialog.compile_stage1_prompt()` to resolve missing report SHAs from SQLite automatically before failing.
    - Unified companion report (`doc_type IN ('afs', 'presentation')`) and SENS (`doc_type = 'sens'`) extraction across `section_capture/audit_dialog.py` and `workflow/export_stage1.py`:
      - For CGR, seamlessly compiles all 41 captured sections (5 Integrated Annual Report [IAR] sections + 36 Annual Financial Statements [AFS] companion sections, ~2.9M chars) into the Stage 1 Forensic Audit Prompt.
    - Cleaned up orphaned code stubs in `workflow/export_stage1.py` and added ticker-specific report resolution in `get_latest_report_sha(conn, ticker=ticker)`.
    - Added regression test `test_cgr_detection_and_stage1_compile` in `tests/test_portfolio_valuation.py`. All 107 tests in the suite pass with exit code 0.

- **Two-Row Responsive Toolbar Layout (section_capture/window.py)**:
  - Addressed toolbar horizontal overflow on standard screen resolutions where right-hand action buttons (`Stored questions`, `Saved sections`, `Audit & Valuation`, `Analyzed Stocks`) collapsed into Qt's `...` overflow menu.
  - Split the single toolbar into two dedicated, non-movable toolbars via `self.addToolBarBreak(Qt.ToolBarArea.TopToolBarArea)`:
    - **Row 1 (`nav_toolbar: "PDF navigation"`)**: Document opening (`New`, `Open PDF`), physical PDF page navigation (`Previous`, `Page [N] of M`, `Next`), Selection mode (`Area (Alt+A)` / `Text (Alt+T)`), and Sector dropdown.
    - **Row 2 (`tools_toolbar: "Tools and analysis"`)**: Zoom & view controls (`Fit page`, `−`, `+`), canvas selection actions (`Clear selection`, `Select page`), and dialog access buttons (`Report map`, `Stored questions`, `Saved sections`, `Audit & Valuation`, `Analyzed Stocks`).
  - Guarantees all controls remain directly visible without button crowding or overflow menus at standard desktop resolutions (>= 1000px width).

- **Company vs Consolidated Statement Disambiguation & Subheading Requirement Fix**:
  - Resolved heading and section collision where `"Statement of cash flows"` (Company statement on page 78, D010) was incorrectly matched by loose substring against `"Consolidated statement of cash flows"` (Group statement on pages 18–76, D005), which already had subsections.
  - Prefixed report map sections in `HeadingComboBox` with their unique section ID (`D005 — Consolidated statement of cash flows`, `D010 — Statement of cash flows`), guaranteeing complete visual clarity and direct, deterministic reverse lookup.
  - Enhanced `find_matching_section()` and `save_package()` to recognize section ID prefixes directly, assigning the exact section ID (`D010`) and cleanly storing the stripped heading (`Statement of cash flows`) in SQLite.
  - Previously, `section_requires_subheading()` only evaluated sections with subsections and performed loose substring matching (`norm_h in c or c in norm_h`), ignoring physical page range overlaps. This falsely flagged D010 as D005 requiring a sub-heading and disabled both `Save Section` and `Save & Run DeepSeek`.
  - Implemented `find_matching_section(mapping, heading, selections)` with rigorous multi-tier priority scoring:
    - Direct: Unique section ID prefix match (`D010 — ...`).
    - Tier 1: Selection physically overlaps section AND exact heading match (`norm_h == c`).
    - Tier 2: Non-overlapping / no selections AND exact heading match (`norm_h == c`).
    - Tier 3: Physical page overlap AND strong fuzzy match (respecting "consolidated" vs separate statement identity).
    - Tier 4: Physical page overlap with no heading specified.
    - Tier 5+: Weak loose match or non-overlapping fuzzy match.
  - Updated `section_requires_subheading()` to evaluate the true target section rather than scanning only subdivided sections.
  - Updated `matching_section_ids()` and `register_subsection()` to accept `heading` to accurately resolve sections and parent subsections when multiple statements share physical pages (e.g., page 78 containing both D009 Changes in Equity and D010 Cash Flows).
  - Formatted subsection lists in warning labels cleanly (`D005 (D005.1 – D005.21)`) rather than dumping all 21 comma-separated IDs across the screen, removing the misconception of concatenation.
  - Added unit test `test_disambiguate_company_vs_consolidated_statements` in `tests/test_report_map.py`. Complete test suite passed (106 tests, exit code 0).

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
    - Implemented `fit_dialog_to_screen()`: adaptively sizes `SavedSectionsDialog`, `ReportMapDialog`, and `QuestionsLedgerDialog` based on `QApplication.primaryScreen().availableGeometry()` (accounting for taskbars and Windows DPI scaling), preventing dialogs from overflowing smaller or scaled displays.
    - Reorganized `SavedSectionsDialog` controls into two clean rows: full-width Section selector row on top, followed by an actions toolbar (`Query Model`, `:nitro`, `Copy prompt`, `Paste response`, `Clear response`), eliminating wide horizontal overflow.
  - All 54 tests passing (exit code 0).
- **OpenRouter Reasoning Mode & Runaway Loop Fix (`section_capture/openrouter.py`)**:
  - Identified root cause of the 198.1s / 131,072 completion token / empty response bug on Section 3: `deepseek/deepseek-v4.1-flash-1017` on OpenRouter defaults to `reasoning: {"default_enabled": true, "default_effort": "high"}`. For complex analytical targets and tables, the model entered a recursive internal reasoning loop that generated 131,072 reasoning tokens without writing the answer `content`, cutting off with `finish_reason: length`.
  - Configured `"reasoning": {"effort": "none"}` in OpenRouter payload: disables unnecessary internal thinking loops and makes the model operate as a pure forensic instruction-following engine, dropping query time from 198.1s to 21.2s and cost by 10x ($0.012 vs $0.122) while generating the full 36,051 character brief.
  - Added safety token ceiling `"max_tokens": 16384` to prevent any future runaway provider billing.
  - Added empty content validation in `query_openrouter`, `map_dialog.py`, and `window.py`: raises an informative exception on `finish_reason: length` and prevents saving 0-character responses to SQLite.
- **Automated Sequential Section Resubmission Engine (`workflow/resubmit_sections.py`)**:
  - Implemented a standalone command-line pipeline to sequentially execute sections through OpenRouter with dynamic questions ledger inheritance:
    - Automatically clears prior responses and resets questions ledger if `--clear` is passed.
    - Dynamically rebuilds each section prompt with the latest `reports.questions_ledger` updated by the preceding section.
    - Captures response time, exact OpenRouter generation stats (cost, prompt/completion tokens), persists outputs to SQLite, and writes formatted markdown briefs to `companies/<sector>/<ticker>/briefs/`.
    - Handles Windows console UTF-8 reconfigure gracefully.
  - Successfully executed all 4 Lewis sections sequentially with `deepseek/deepseek-v4.1-flash-1017`:
    - **Section 01 (Chairman's Report)**: 21.04s | $0.0004 | 8,198 tok | 11,617 chars | Ledger: 2,261 chars
    - **Section 02 (CEO's Report)**: 53.06s | $0.0022 | 10,460 tok | 18,583 chars | Ledger: 5,374 chars
    - **Section 03 (Strategy & Targets)**: 38.48s | $0.0024 | 11,209 tok | 21,392 chars | Ledger: 7,586 chars
- **GUI Integration for Stage 1 (Forensic Audit) & Stage 2 (Valuation Note) and SQLite Persistence**:
  - **Database Persistence (`section_capture/db.py`)**:
    - Extended SQLite `reports` table schema with automatic migration:
      `stage1_prompt`, `stage1_response`, `stage1_updated_at`, `stage2_prompt`, `stage2_response`, `stage2_updated_at`.
    - Added persistence helpers: `save_stage1_report()`, `get_stage1_report()`, `save_stage2_report()`, `get_stage2_report()`.
  - **Modularized Workflow Compilation (`workflow/`)**:
    - Extracted `build_stage1_prompt_content()` in `workflow/export_stage1.py`.
    - Extracted `build_stage2_prompt_content()` in `workflow/generate_stage2.py` embedding the 99% confidence prior rule.
  - **Dedicated Workflow Dialog (`section_capture/audit_dialog.py`)**:
    - Built `AuditValuationDialog` with responsive layout (`fit_dialog_to_screen`) and two tabs:
      - **Tab 1: Stage 1 Cognitive Forensic Audit**: Side-by-side prompt compilation / preview and response editor. Single-click actions: "Compile from SQLite", "Copy prompt", "Paste from clipboard", "Load from disk", and "Save Response to DB" (persists to SQLite and writes to disk).
      - **Tab 2: Stage 2 Institutional Valuation**: Side-by-side prompt generation (incorporating Stage 1 ground truth as 99% prior) and final valuation report editor. Actions: "Generate Stage 2 Prompt", "Copy prompt", "Open PDF folder", "Paste from clipboard", "Save Final Report to DB".
  - **Main Window Integration (`section_capture/window.py` & `map_dialog.py`)**:
    - Added `"Audit && Valuation"` action to the top toolbar in `window.py`.
    - Added `"Audit & Valuation →"` action button in `SavedSectionsDialog` to transition directly from section review to Stage 1 & 2 execution.

- **Lewis Group (LEW) 3-Tier Pipeline Execution & Forensic Contrast**:
  - All 14 sections captured in SQLite with DeepSeek Flash reading briefs.
  - Stage 1 Forensic Audit executed by Gemini 4 Argon, saved to `companies/retail/LEW/briefs/FY26/LEW_FY26_stage1_audit_response.md` (25,093 chars) and SQLite `reports.stage1_response`.
  - Stage 2 Institutional Valuation executed by Gemini 4 Argon with 99% confidence prior rule, saved to `companies/retail/LEW/briefs/FY26/LEW_FY26_stage2_valuation_note.md` (46,706 chars) and SQLite `reports.stage2_response`.
  - Evaluated against raw PDF single-shot prompt: Demonstrated why raw PDF produced a flawed BUY thesis at R108.50 (+50.2% TSR) due to hallucinated gross margins (+30 bps to 43.7%), ignoring R961m arrears hidden inside "satisfactory paid" accounts, R1.2bn working capital drain, and debt-funded dividends. In contrast, the 3-Tier Pipeline established an institutional HOLD rating at R84.50 (+18.9% TSR), factoring in 40–42% guided gross margin compression and credit book seasoning.

- **Stage 2 Prompt Standardization & Monitoring Triggers Upgrade (`workflow/generate_stage2.py`)**:
  - Mandated an **Executive Valuation Summary Card** in Section 1 for both Retail and Mining with standardized fields: Target Price, Current Reference Price, Recommendation, Implied Upside, Dividend Yield, and 12M TSR.
  - Mandated an explicit **Section 6: Actionable Portfolio Monitoring Triggers & Catalysts ("What to Watch For That Will Move the Stock")**:
    - Operational & Financial Red Lines (e.g. collection rate dipping below bonus hurdle, margin floors, working capital burn).
    - Quantified Sensitivity Impacts (e.g. "Every 75 bps swing in gross margin alters HEPS by X cents and fair value by R Y/share").
    - Re-Rating Catalysts (milestones required to trigger an upgrade).
    - Upcoming Milestones & Reporting Dates (key calendar dates for portfolio managers).

- **Database Valuation Schema & Auto-Extraction (`section_capture/db.py`)**:
  - Extended SQLite `reports` table with automatic migration and backfill for:
    `target_price_zar REAL`, `reference_price_zar REAL`, `recommendation TEXT`, `upside_pct REAL`, `dividend_yield_pct REAL`, `tsr_pct REAL`, `monitoring_triggers TEXT`, `valuation_summary_json TEXT`.
  - Implemented `parse_valuation_summary()` to auto-extract executive valuation metrics and monitoring triggers from Markdown reports.
  - Integrated auto-extraction into `save_stage2_report()`, persisting parsed metrics whenever a Stage 2 report is saved.
  - Implemented `get_analyzed_stocks()` returning structured coverage metadata and status across all companies in SQLite.
  - Added company profile inference (`detect_company_meta()`) resolving tickers, corporate titles, and sectors.

- **Portfolio Coverage & Monitoring Dashboard GUI (`section_capture/portfolio_view.py`)**:
  - Built interactive `PortfolioView` widget and `PortfolioCoverageDialog`:
    - **Header & Filter Bar**: Shows tracked universe statistics (e.g. `Coverage Universe: 1 Active Valuation · 2 Total Assets Tracked`), search filter, sector filter dropdown, recommendation rating dropdown, refresh, and "Copy Universe Table" in Markdown.
    - **Top Table (`QTableWidget`)**: Displays Ticker, Company Name, Sector, Current Price, 12M Target, Implied Upside, Forward Yield, 12M TSR, color-coded Recommendation Badges (Green BUY, Amber HOLD, Red SELL, Gray IN PROGRESS), Section Status, and Analysis Date.
    - **Bottom Details Panel ("What to Watch For That Will Move the Stock")**: Reactive panel rendering the selected company's KPI summary cards, actionable monitoring triggers with quantified sensitivity rules, and calendar milestones.
    - **Quick Actions**: "View Full Valuation Note", "View Stage 1 Audit", "Copy Triggers".
  - **Application Integration**:
    - Integrated as Tab 3 ("Analyzed Stocks & Portfolio Coverage") in `AuditValuationDialog`.
    - Added direct `"Analyzed Stocks"` toolbar action in `CaptureWindow` (accessible anytime, even without an open PDF).
  - Added **"Open prompt folder"** action in both Stage 1 and Stage 2 tabs (`section_capture/audit_dialog.py`) to open Windows Explorer with the generated prompt markdown file pre-selected, enabling instant drag-and-drop file upload into Gemini 4 Argon for prompts that exceed web chat textbox paste limits (e.g. PAN's 847k character working paper prompt).
  - **PAN FY26 Briefs Cleanup & Canonical Standardization**:
    - Inspected `companies/mining/PAN/briefs/FY26/` and purged redundant/experimental files (`experiment2_argon_ledger_audit_prompt.md`, `FY26-2-year-analyst-valuation-brief.md`, `gemini_hybrid_prompt.md`, `section_01_D002_deepseek_response.md`, test artifacts, and unversioned aliases).
    - Preserved and standardized canonical files:
      - `PAN_FY26_stage1_forensic_prompt.md` (847,119 bytes)
      - `PAN_FY26_stage1_audit_response.md` (54,253 bytes)
      - `PAN_FY26_stage2_valuation_prompt.md` (58,665 bytes)
    - Synchronized SQLite `reports` table row for PAN with verified Stage 1 audit and Stage 2 prompt.
    - Updated `open_stage1_folder()` and `open_stage2_folder()` in `section_capture/audit_dialog.py` to ensure prompt files are saved to disk directly if prompt text is present.
    - Isolated `briefs_dir` during test runs so pytest never writes to project company brief folders.
  - **In-GUI Company Scaffolding ('New' Action)**:
    - Added a **"New"** button to the capture app toolbar positioned immediately to the left of "Open PDF".
    - Created `NewCompanyDialog` in `section_capture/new_company_dialog.py` connecting GUI inputs to `new_company.create_company`:
      - Auto-capitalizes and validates ticker symbols (e.g. `SBK`, `SOL`, `MTN`, `CPI`).
      - Sector selection dropdown (`Mining`, `Retail`, `Finance`, `Telcos`).
      - Company name input with sensible fallbacks.
      - Optional PDF report file picker: automatically copies the selected PDF into `companies/<sector>/<ticker>/sources/` and immediately opens the PDF in `CaptureWindow` with the sector combobox synchronized.
      - If no PDF is selected, scaffolds the directory tree (`sources/`, `models/`, `research/`, `briefs/`), `config.py`, `run.py`, and interactive Jupyter sandbox `<ticker>_sandbox.ipynb`, and opens the `sources` folder in Windows Explorer.
    - Added unit and GUI tests in `tests/test_capture.py` verifying scaffolding, validation, and PDF opening.
  - **Manual Section Mapping, Rapid Page Flipping & Capture Shortcuts**:
    - **Instant PDF Open**: Removed automatic heuristic prescan on opening a PDF report (`open_pdf(path, auto_scan=False)`). PDF opens instantly without waiting for a 54-page background scan.
    - **Interactive Manual Section Map Builder**:
      - Upgraded `ReportMapDialog` (`section_capture/map_dialog.py`) to an interactive Section Map editor with table of mapped sections (`ID`, `Section Title`, `Start`, `End`).
      - Added "Add from selected text on PDF" and manual input row to rapidly log section headings from the Table of Contents or report pages.
      - Implemented `build_manual_section_map()` (`section_capture/report_map.py`) ensuring clean, contiguous, 100% valid partitions covering pages 1 to `page_count` with status `'manual_outline'`.
      - "Save Map & Update Dropdown" persists the manual map to SQLite and automatically synchronizes the Section Heading combobox options.
    - **Combobox Dropdown Kept & Populated**: Maintained `HeadingComboBox` in the sidebar, now cleanly populated from the manual section map so analysts can quickly pick the target section during capture.
    - **Keyboard Shortcuts for Selection Modes**:
      - `Alt+A`: switches canvas to Area selection.
      - `Alt+T`: switches canvas to Text selection.
      - Updated mode dropdown labels to show shortcuts (`Area selection (Alt+A)`, `Text selection (Alt+T)`).
    - **Rapid Page Navigation via `Tab` / `Shift+Tab`**:
      - Pressing `Tab` advances to the next page and `Shift+Tab` / `Backtab` moves to the previous page when focus is on the PDF canvas or window (safely ignored when typing in editable inputs).
    - **Sidebar Text Transfer & Section Buttons**:
      - Section heading row: `[Use text]` (fills heading from selected canvas text) and `[New section]` (clears headings, resets pending selections, focuses heading edit).
      - Sub-heading row: `[Use text]` (fills sub-heading from selected canvas text) and `[New subsection]` (preserves parent heading, clears sub-heading, focuses sub-heading edit).
    - **Refined Subheading Requirement Logic**:
      - Updated `section_requires_subheading()` so selecting or typing a new distinct major section (e.g. `MINERAL RESOURCES`) does not get falsely blocked by older nearby subsections.
    - **Stable Section IDs with `-ins` Suffix on Mid-Capture Insertions**:
      - Implemented `assign_section_ids()` in `section_capture/report_map.py`: when a new section is inserted into an existing report map during capture, existing section IDs are preserved without shifting (e.g. `D003` remains `D003`).
      - Newly inserted sections receive an explicit `-ins` suffix (e.g. `D001-ins`, `D002-ins`, `D002-ins2`) based on their predecessor.
      - Updated `ReportMapDialog` (`section_capture/map_dialog.py`) to preserve established IDs, preview the `-ins` ID dynamically in the table, and save stable contiguous partitions.
      - Updated prefix stripping regexes in `section_capture/packages.py` and `section_capture/report_map.py` (`r"^D[a-zA-Z0-9_\-\.]+\s*[—:\-]\s*"`) to cleanly handle `-ins` IDs without stripping section titles.
    - **Orion Minerals (ORN) Reset**: Purged all 7 previously captured sections and DeepSeek responses from SQLite, cleared `report_map_json` and `questions_ledger`, and reset valuation fields for ORN. The original report PDF remains intact in `companies/mining/ORN/sources/` ready for a completely fresh capture workflow.
    - **Remember Last Opened Folder in 'Open PDF'**: Updated `choose_pdf()` and `open_pdf()` in `section_capture/window.py` to track the parent directory of the opened PDF and persist it using `QSettings`. When clicking 'Open PDF', the file dialog opens directly in the folder of the last opened PDF report (or the newly scaffolded company's `sources/` folder).
    - **Global Tab & Shift+Tab Page Flipping Filter**: Installed the event filter at the `QApplication` instance level and directly on `canvas.viewport()` (with automatic cleanup on window close/destruction) so `Tab` and `Shift+Tab` reliably flip PDF pages when clicking or interacting with the canvas, while preserving standard focus navigation inside text inputs and modal dialogs.
    - **Modeless (Non-Modal) Report Map Dialog**: Converted `ReportMapDialog` from a blocking modal dialog (`.exec()`) to a modeless floating window (`.show()`). Analysts can now keep the Report Map open side-by-side with the main window, flip pages with `Tab`, highlight text on the canvas, and click "Add from selected text on PDF" without closing and reopening the dialog for each section. Automatically synchronizes the dialog's page spinner with the main window's current PDF page.
    - **Initial Outline Mapping vs Mid-Capture Insert Architecture**:
      - **First Mapping in Report Map Dialog**: Removed `-ins` suffix generation during initial mapping. Sections added in `ReportMapDialog` from Table of Contents or outline are cleanly numbered sequentially (`D001`, `D002`, `D003`, `D004`...).
      - **Insert Functionality on Capture Section Page**: Replaced the `New section` button next to Section heading with an `[ Insert ]` button (`InsertSectionDialog`).
      - Clicking `[ Insert ]` on the capture section page opens a dialog pre-filled with selected canvas text or typed heading and current PDF page. It calculates the predecessor section, previews the assigned ID (e.g. `D002-ins`) and boundary partition live, updates `report_map` in SQLite, refreshes heading dropdown options, and activates the new section for immediate capture without shifting following section IDs (`D003`, `D004`, etc. remain untouched).
      - **Removed Single-Section-Per-Page Constraint**: Removed constraints blocking multiple sections from starting on the same physical PDF page (common in 2-up spreads like the Consolidated Statement of Profit or Loss and Consolidated Statement of Financial Position on physical page 45). Updated `validate_map()`, `build_manual_section_map()`, `preview_inserted_section_id()`, and `insert_section_into_report_map()` so co-located sections share start pages cleanly and display accurate partitions.
      - **Markdown Table Support for Executive Valuation Cards**: Enhanced `parse_valuation_summary()` in `section_capture/db.py` to support Executive Valuation Summary Cards rendered with Markdown table pipes (`|`) in addition to colon bullet lists. Auto-backfilled ORN in `documents/analysis.sqlite` with Target Price `R0.21`, Reference Price `R0.28`, Recommendation `SELL` (-26.1% downside), and 5,651 chars of monitoring triggers.
    - **Cross-Machine Portable Folder Persistence in SQLite (No Registry)**:
      - Completely removed all dependencies on Windows Registry / `QSettings`.
      - Added `app_state` key-value table to `documents/analysis.sqlite` (`key`, `value`, `updated_at`).
      - Implemented `save_last_opened_dir()` and `load_last_opened_dir()` in `section_capture/db.py`: paths within the project directory are stored as normalized relative paths (e.g. `companies/mining/ORN/sources`), making database backups, git checkouts, and multi-machine moves completely portable.
      - On load, falls back to the most recently updated report in `reports` table if no preference is explicitly stored.
      - Fully isolated test executions using SQLite test fixtures so running unit tests never pollutes or alters the production active directory.
    - **Post-Annual-Report SENS & Continuous Disclosures Integration**:
      - **Database Schema & Relational Linking (`section_capture/db.py`)**:
        - Extended `reports` table schema with `parent_report_sha256 TEXT`, `doc_type TEXT NOT NULL DEFAULT 'annual_report'`, and `announcement_date TEXT`.
        - Implemented auto-detection `detect_doc_type_and_date(path_or_filename)` extracting announcement dates (`YYYYMMDD` or `YYYY-MM-DD`) and identifying SENS notices in `sources/sens/` or via continuous disclosure naming.
        - Implemented `auto_link_parent_report()` and `link_sens_report()` to bind subsequent SENS notices to the primary Annual Report.
      - **Questions Ledger Inheritance & Bi-Directional Synchronization**:
        - SENS notices automatically inherit the full active `questions_ledger` from the primary Annual Report upon creation/linking.
        - When DeepSeek Flash processes a SENS section and outputs Section 4 (`Updated Open Questions Ledger`), the extracted ledger updates both the SENS report and synchronizes back to the parent Annual Report in SQLite.
      - **In-App Document Switcher & SENS Management (`section_capture/window.py`)**:
        - Added an interactive **Document Switcher** (`self.doc_selector`) and **`+ Add SENS Notice`** button directly above the PDF canvas.
        - Dropdown groups and displays the primary `[Annual Report]` alongside all linked subsequent notices (`[SENS 2026-10-19]`), enabling seamless instant canvas switching.
        - SENS captures automatically generate clean section IDs (`SENS-01`, `SENS-02`) and pre-populate relevant heading suggestions.
      - **Multi-Document Stage 1 & Stage 2 Pipeline Integration (`workflow/export_stage1.py`, `workflow/generate_stage2.py`, `section_capture/audit_dialog.py`)**:
        - Upgraded `build_stage1_prompt_content()` and `compile_stage1_prompt()` to assemble a unified two-part working paper dossier:
          - `PART 1: PRIMARY FINANCIAL DISCLOSURE` (Annual Report sections).
          - `PART 2: SUBSEQUENT SENS & CONTINUOUS DISCLOSURE ANNOUNCEMENTS` (post-year-end SENS sections in chronological order).
        - Directs Gemini 4 Argon to reconcile post-balance-sheet cash runway, funding CPs, and revised guidance.
        - Upgraded Stage 2 valuation prompt compiler to factor post-balance-sheet SENS determinations into baseline cash, net debt, and forecast models.
      - **Simplified SENS Valuation Update & Re-Rating (`workflow/generate_sens_update.py`)**:
        - Built a token-efficient prompt generator combining the established Final Institutional Valuation Report (from SQLite `reports.stage2_response`) with the attached SENS PDF.
        - Directs Gemini 4 Argon to analyze the attached SENS PDF directly (without requiring manual section cropping), evaluate the financial/operational impact against the baseline report, update the Executive Valuation Summary Card (ZAR target price, recommendation), re-rate the Section 6 Monitoring Triggers, and output a new updated valuation note.
        - Integrated the **`⚡ Generate SENS Update Prompt`** button in Tab 2 of `AuditValuationDialog`.
        - **Baseline Valuation Safeguarding (Disk & SQLite)**:
          - The original annual report valuation note is permanently preserved on disk as `companies/<SECTOR>/<TICKER>/briefs/<PERIOD>/<TICKER>_<PERIOD>_stage2_valuation_note_baseline.md`.
          - In SQLite, the initial valuation response is preserved in `reports.stage2_baseline_response` and `stage2_baseline_updated_at`. When subsequent SENS valuation updates are saved, the active `stage2_response` updates with the new post-SENS note, while the baseline remains permanently archived and protected from overwrite.
          - Fixed `save_stage2_report()` query in `section_capture/db.py` to retrieve all columns (`SELECT *`) ensuring baseline comparisons run cleanly.
        - Generated the SENS update prompt for Orion Minerals (`ORN`) at `companies/mining/ORN/briefs/FY26/ORN_FY26_stage2_sens_update_prompt.md`.
    - **Dynamic Company & Ticker Dropdown in Valuation Dialog (`section_capture/audit_dialog.py`, `portfolio_view.py`, `window.py`)**:
      - **Always-Enabled Audit & Valuation**: Enabled the `Audit & Valuation` toolbar action regardless of whether a PDF is actively loaded in the canvas, eliminating the disabled state and `COMPANY (Retail) - No report loaded` fallback.
      - **Company / Ticker Dropdown Selector (`QComboBox`)**: Added an interactive selector in the dialog header displaying all tracked companies across SQLite and filesystem (`ORN — Orion Minerals (Mining) [Valued · R0.21 Target]`, `PAN — Pan African Resources (Mining) [Audited (19 sec)]`, `LEW — Lewis Group Limited (Retail) [Captured (4 sec)]`, etc.).
      - **Automatic Discovery & State Reloading**: Automatically discovers reports, selects the most active stock by default when opening without a PDF, and dynamically updates dialog title, sector badge, briefs directory, Stage 1 / Stage 2 prompt & response editors, and status labels upon selection change.
      - **`Open in Canvas` Action**: Added one-click canvas loading button allowing users to open the selected company's PDF report directly in the main viewer canvas from the dialog.
      - **Portfolio View Stage 2 Jump**: Added `⚡ Go to Stage 2 Valuation` button and table double-click navigation in `PortfolioView` (Tab 3) that instantly switches the active company in the dialog and navigates directly to Tab 2 (Stage 2 Valuation Note).
    - **Multi-Column Valuation Summary Card & Post-SENS Re-Rating Parser (`section_capture/db.py`)**:
      - Fixed `parse_valuation_summary()` to correctly distinguish between **Prior Stage 2 Determinations** and **Updated Stage 2-U Determinations** in comparison tables generated by Argon (such as `| Recommendation | SELL | HOLD (UPGRADED FROM SELL) |`).
      - Updated cell extraction to evaluate determination columns from right to left, preventing the prior rating/price from preempting the newly updated rating/price.
      - Backfilled `documents/analysis.sqlite` for ORN: rating successfully upgraded from `SELL` to `HOLD`, Target Price updated to `R0.26` (up +23.8% from R0.21), and implied upside updated to `-8.5%` (from -26.1%).
  - **First-Class REIT (Real Estate Investment Trust) Sector Implementation**:
    - **Sector Architecture & Scaffolding (`companies/reit/`)**:
      - Created `companies/reit/__init__.py` and `companies/reit/README.md` documenting JSE REIT dynamics, SA REIT Best Practice Recommendations (BPR), and key tickers.
      - Registered `"reit"` in `SECTORS` (`companies/__init__.py`) and `SUPPORTED_SECTORS` (`section_capture/packages.py`).
      - Added directory auto-detection for `reit`, `property`, `real_estate`, `reits` in `detect_sector_from_path()`.
    - **Forensic REIT Sector Prompts (`prompts/reit/`)**:
      - `00-report-orientation/v1.0.0/prompt.md`: Major-section map orientation focusing on SA REIT disclosures, property portfolio performance, debt/treasury schedules, and valuation notes.
      - `12-analyst-reading-brief/v1.1.0/prompt.md`: Deep forensic prompt centered on:
        1. *Distributable Income & DIPS Bridge*: IFRS profit reconciliations, straight-line lease accrual exclusions, fair-value property movements, derivative MTM adjustments, and dividend payout ratios.
        2. *Property Portfolio Operations*: Like-for-like NPI growth, WALE (GLA & revenue), reversion rates, sub-sector vacancies (Retail, Office, Industrial/Logistics), and municipal recovery ratios.
        3. *LTV & Capital Structure*: Nominal vs look-through LTV, interest rate hedging ratios (>70% benchmark), debt tenors, weighted cost of debt, and ICR covenant headroom.
        4. *Fair Value & Cap Rates*: Independent vs directors' valuations, exit cap rates, discount rates, and NAV discounts/premiums.
        5. *Developments & Capital Allocation*: Maintenance capex vs tenant installations (TI) vs development pipelines, and disposal cap rates.
    - **Scaffolding Tooling (`new_company.py`, `section_capture/new_company_dialog.py`)**:
      - Added `reit` choice to CLI and GUI company generators.
      - Built tailored Jupyter sandbox template (`<ticker>_sandbox.ipynb`) with REIT-specific financial parameters (contractual escalations, vacancy rates, exit cap rates, LTV, payout ratios).
    - **Database & Known Companies (`section_capture/db.py`)**:
      - Populated prominent JSE REIT tickers in `KNOWN_COMPANIES`: `GRT` (Growthpoint), `RDF` (Redefine), `VKE` (Vukile), `HYP` (Hyprop), `ATT` (Attacq), `FFB` (Fortress), `EQU` (Equites), `RES` (Resilient).
      - Added title formatting fallback for `{TICKER} Properties`.
    - **UI Integration across PySide6 App**:
      - `section_capture/window.py`: Added `Sector: REIT` to the main toolbar sector dropdown.
      - `section_capture/portfolio_view.py`: Added `REIT` filter and display rendering in the portfolio table.
      - `section_capture/audit_dialog.py`: Added REIT path detection, folder discovery, and emerald-green sector badge styling (`#ecfdf5` / `#065f46`).
    - **Workflow Compilers (`workflow/export_stage1.py`, `workflow/generate_stage2.py`)**:
      - Configured Stage 1 persona: `Managing Director and Senior Forensic Real Estate & REIT Financial Auditor`.
      - Configured Stage 2 persona: `Managing Director & Head of Listed Property & REIT Equity Research` directing SOTP NAV, DIPS bridges, and exit cap rate sensitivities.
    - **Automated Test Coverage (`tests/test_capture.py`)**:
      - Added path detection, prompt existence, prompt content verification, and UI combo tests for `reit`.
  - **Interactive Chat Instruction Text Boxes & 1-Click Clipboard Actions (`section_capture/audit_dialog.py`)**:
    - Embedded dedicated **Chat Instruction** text fields (`QLineEdit`) directly into the Stage 1 and Stage 2 callout headers.
    - Added 1-click **`📋 Copy chat text`** buttons next to each text box with instant temporary `✓ Copied!` visual feedback and status bar confirmation.
    - Pre-configured tailored execution directives:
      - **Stage 1**: `"Please execute the Stage 1 Forensic Audit for {company_title} ({ticker}) as detailed in the attached prompt file. Follow all instructions, verification rules, and output structures specified in the document."`
      - **Stage 2 (Standard)**: `"Please execute the Stage 2 Institutional Valuation Note for {company_title} ({ticker}) as detailed in the attached prompt file and accompanying PDF report. Follow all valuation guidelines, forecast models, and output tables specified in the document."`
      - **Stage 2-U (SENS Update)**: Automatically switches instruction when `⚡ Generate SENS Update Prompt` is clicked to: `"Please execute the Stage 2-U SENS Valuation Update for {company_title} ({ticker}) as detailed in the attached prompt file and accompanying SENS PDF. Re-rate target price, recommendations, and monitoring triggers against the baseline report."`
    - Dynamically updates company title and ticker in the instructions when switching companies via the dropdown.
    - Enhanced `open_stage1_folder()` and `open_stage2_folder()` status messages to remind users to drag & drop the file, then paste the Chat instruction.
    - Added test coverage in `tests/test_portfolio_valuation.py`.
  - **SENS Plain Text (.txt) Ingestion & Completed Archival Engine (`workflow/generate_sens_update.py`, `section_capture/audit_dialog.py`)**:
    - **Multi-Format SENS Discovery**: Expanded `generate_sens_update_prompt()` to discover both `.pdf` and `.txt` / `.text` / `.md` continuous disclosure announcements in `companies/<SECTOR>/<TICKER>/sources/sens/`.
    - **In-Prompt Text Embedding**: When SENS notices are in plain text (e.g. APF's 8 post-year-end notices: debt capital reductions, JSE censure, AGM outcomes, and the R385m KPMG Crescent property disposal), the complete text is embedded directly into Section 2 of `stage2_sens_update_prompt.md` in chronological sequence. Eliminates the need to upload separate SENS attachments into chat.
    - **Sector Persona Tailoring**: Added REIT equity research persona (`Managing Director & Head of Listed Property & REIT Equity Research`) alongside retail and mining personas.
    - **Automatic & Manual Archival (`completed/`)**:
      - Implemented `get_sens_completed_dir()` and `move_analyzed_sens_files()` to move analyzed SENS notices into `sources/sens/completed/` (supporting `sources/sens_completed` fallback).
      - Added **`📦 Move SENS to Completed`** button in Tab 2 of `AuditValuationDialog` for manual archiving.
      - Automated auto-archiving of pending SENS notices when saving an analyzed Stage 2-U report (`save_stage2_response()`).
    - Added unit and GUI tests in `tests/test_portfolio_valuation.py`.
  - **Portfolio Multi-Column Table Parser & Dynamic Display Synchronization Fix**:
    - **Reconstructed Markdown Multi-Line Table Rows (`section_capture/db.py`)**: Fixed `parse_valuation_summary()` to correctly accumulate table rows whose cells contain internal line breaks (e.g. Gemini's markdown tables formatted with `\n\n` before pipe separators). Previously, unclosed table rows were flushed prematurely, causing the updated Stage 2-U determination columns to be severed from the metric heading.
    - **Cell-Boundary Scoped Determinations**: Scoped price and percentage regex extraction strictly to determination cells (`cells[1:-1]`), completely isolating determinations from trailing commentary columns (e.g. preventing commentary phrases like `"swaps become >100% over-hedged"` or `"KPMG rent reset (R99.52/m²)"` from corrupting the target price or upside percentage).
    - **Live Header & Portfolio View Sync (`section_capture/audit_dialog.py`)**:
      - Updated `save_stage2_response()` and tab switching (`_on_tab_changed`) to re-query `discover_available_companies()` and refresh both `company_combo` and `tab_portfolio.refresh()`.
      - Backfilled `documents/analysis.sqlite` for Accelerate Property Fund (`APF`): Target Price updated from R0.48 to **R0.42** (downgraded on KPMG Crescent rent reset and ICR collapse), Implied Upside updated from +100% to **-30.0%**, Reference Price set to **R0.60**, and Recommendation set to **SELL**.
  - **Full Valuation Note Markdown & Table Rendering Normalization (`section_capture/portfolio_view.py`)**:
    - **Diagnosed QTextBrowser Markdown Collapse Glitch**:
      - Discovered why the Full Valuation Note dialog (`MarkdownViewerDialog`) showed broken table pipes and collapsed paragraphs into `APFAPFERMA`:
        1. **Broken Table Rows**: Gemini Argon generated Markdown tables with blank lines (`\n\n`) between cells. Under standard CommonMark / Qt Markdown, a blank line immediately terminates a table, spilling remaining cells into raw text paragraphs with pipe delimiters (`| |`).
        2. **Unclosed `<br>` HTML Tag Swallowing**: Gemini Argon outputted unclosed `<br>` tags inside table cells (e.g., `**SELL**<br>`, `**-20.0%**<br>`). In Qt's CommonMark HTML processor, encountering unclosed `<br>` alongside table pipes and angle brackets (e.g. `>100% over-hedged`) trips Qt into an unclosed HTML block state. This swallowed all regular text paragraphs, headings, and bullet points, leaving behind only inline backtick code snippets merged together (`APF` + `APFE` + `RMA` -> `APFAPFERMA`).
    - **Implemented `normalize_markdown_for_qt()`**:
      - Automatically converts unclosed `<br>` tags to valid self-closing `<br/>`.
      - Automatically stitches broken multi-line table rows separated by `\n\n` back into clean single-line Markdown table rows.
      - Integrated normalization into `MarkdownViewerDialog` and the portfolio `triggers_browser`.
    - Added automated unit test in `tests/test_portfolio_valuation.py`.
    - **Standardized Machine-Readable JSON Schema & Strict Prompt Constraints (`workflow/generate_stage2.py`, `workflow/generate_sens_update.py`, `section_capture/db.py`)**:
    - **Prompt Generators Standardized (Recency Weighting & Negative Constraints)**:
      - Enforced a mandatory ````json ... ```` summary block opening Section 1 with native numeric floats (`target_price_zar`, `reference_price_zar`, `implied_upside_pct`, `forward_dividend_yield_pct`, `projected_12m_tsr_pct`, and `recommendation`).
      - Placed the **`CRITICAL OUTPUT FORMATTING CONSTRAINTS (STRICTLY ENFORCED)`** section as the very last section/sentence of both `generate_stage2.py` and `generate_sens_update.py` to maximize prompt recency weighting.
      - Enforced negative constraints: zero HTML tags (`<br>`, `<span>`), single-line Markdown table rows, no commentary inside numeric cells, and no arbitrary backticks around numbers.
    - **Fast-Path JSON Parsing Engine (`section_capture/db.py`)**:
      - Added high-speed JSON summary block extraction to `parse_valuation_summary()` using `json.loads()`, bypassing regex ambiguity entirely.
      - Maintained seamless fallback to table and bullet regex parsing for full backward compatibility with legacy reports.
      - Guarded table regex determinations to prevent overwriting validated JSON metrics.
    - Added comprehensive unit tests in `tests/test_portfolio_valuation.py`.
    - All 92 unit and GUI tests pass (exit code 0).
  - **Live Execution & Ingestion of Pan African Resources (`PAN`) Stage 2 Valuation**:
    - Gemini 4 Argon successfully generated the standardized Stage 2 report following the new schema:
      - Opened Section 1 with the exact machine-readable JSON summary block.
      - Generated full 2-year forecast, probability-weighted SOTP DCF, and 44,200 characters of institutional equity research note.
    - Saved to SQLite `reports` table via Tab 2 in `AuditValuationDialog`:
      - **Target Price**: **R43.50** (Probability-weighted SOTP DCF across Scenario A & B).
      - **Reference Price**: **R30.69** (90-day VWAP institutional anchor).
      - **Recommendation**: **BUY** (High conviction cash-flow inflection).
      - **Implied Upside**: **+41.7%** (+105.8% vs spot R21.14).
      - **Forward Dividend Yield**: **5.9%** (Forecast R1.80/share).
      - **12-Month TSR**: **+47.6%**.
      - **Monitoring Triggers**: 7,590 characters of structured downside red lines, margin triggers, MTR commissioning milestones, and reporting calendar dates.
    - Coverage universe now actively tracks 4 fully analyzed assets across 3 sectors (`PAN`, `APF`, `ORN`, `LEW`).
  - **IT Sector Architecture & iOCO Limited (IOC) Scaffolding**:
    - **Sector Registries & Discovery**:
      - Added `"it"` to `SECTORS` in `companies/__init__.py`, `SUPPORTED_SECTORS` in `new_company.py`, and `section_capture/packages.py`.
      - Expanded `detect_sector_from_path()` to detect `/it/`, `\it\`, `/tech/`, `\tech\`, `it`, `tech`, `technology`.
      - Configured bi-directional alias resolution between `IOC` and `IOCO` in `companies/__init__.py` and `KNOWN_COMPANIES` in `section_capture/db.py`.
    - **Targeted Substring Bug Fix in `detect_company_meta()` (`section_capture/db.py`)**:
      - Resolved regex false-positive where any path containing `/companies/` matched `PAN` (`comPANies`).
      - Structured directory path extraction (`parts[idx + 1]`, `parts[idx + 2]`) is checked first, followed by word-boundary matching on file names.
    - **Dedicated IT Sector Prompts**:
      - `prompts/it/00-report-orientation/v1.0.0/prompt.md`: Structured for IT services, cloud architecture, recurring revenue streams, contract assets, WIP, and software capitalization.
      - `prompts/it/12-analyst-reading-brief/v1.1.0/prompt.md`: Deep forensic prompt focusing on ARR/MRR mix, billable consultant utilization rates, IFRS 15 contract assets/liabilities, capitalized software development (IAS 38), and legacy litigation provisions.
    - **Forensic Pipeline & Valuation Persona Updates**:
      - `workflow/export_stage1.py`: IT persona (`Managing Director and Senior Forensic Technology & IT Services Financial Auditor`).
      - `workflow/generate_stage2.py`: IT persona (`Managing Director & Head of Technology & IT Services Equity Research`), 2-year forecast modeling (ARR %, billable consultant utilization, contract assets/liabilities, FCFE bridge, SOTP/DCF table), with canonical `"sector": "it"` in JSON summary block.
      - `workflow/generate_sens_update.py`: Added IT persona and `Technology / IT Services` display.
    - **UI Badging & Filters**:
      - Configured `Sector: IT` in `section_capture/window.py` and `section_capture/new_company_dialog.py`.
      - Added `IT` filter and display in `section_capture/portfolio_view.py`.
      - Added tech indigo badge styling (`#e0e7ff` / `#3730a3`) in `section_capture/audit_dialog.py`.
    - **Company Hub Initialized**:
      - Scaffolding complete for `companies/it/IOC/` (`sources/`, `briefs/`, `models/`, `research/`).
    - All 93 unit and GUI tests passing (exit code 0).

  - **Centralized Sector Registry & Automated Scaffolding Engine (`companies/sectors.py`, `new_sector.py`, `docs/SECTOR_ONBOARDING.md`)**:
    - **Single Source of Truth (`companies/sectors.py`)**:
      - Replaced hardcoded sector lists across 8+ modules with a centralized `SectorConfig` registry.
      - Tracks canonical `code`, `display_name`, `short_label`, UI badge styles (`badge_bg`, `badge_fg`, `badge_border`), personas (`stage1_persona`, `stage2_persona`, `sens_persona`), and path aliases.
      - Integrated dynamic sector discovery across:
        - `companies/__init__.py`: `SECTORS = get_all_sector_codes()`.
        - `new_company.py` & `section_capture/packages.py`: Dynamic sector validation and alias path resolution.
        - `section_capture/window.py` & `section_capture/new_company_dialog.py`: Dynamic sector dropdown population.
        - `section_capture/portfolio_view.py`: Dynamic filter combo population and short label formatting.
        - `section_capture/audit_dialog.py`: Dynamic badge CSS styling and label generation.
        - `workflow/export_stage1.py` & `workflow/generate_sens_update.py`: Dynamic persona assignment.
    - **Sector Scaffolding CLI (`new_sector.py`)**:
      - Single-command sector onboarding: `python new_sector.py <code_name> --name "..." --short "..." --aliases ...`.
      - Automatically registers sector in `companies/sectors.py`, generates `prompts/<sector>/00-report-orientation/` and `prompts/<sector>/12-analyst-reading-brief/`, and initializes `companies/<sector>/__init__.py`.
    - **Standard Operating Procedure (`docs/SECTOR_ONBOARDING.md`)**:
      - Documented 2-minute onboarding protocol, sector-specific forensic focus areas (Pharma, Industrials, Banking, Energy, Agriculture), ticker matching safeguards, and targeted testing protocols.
      - Integrated into `AGENTS.md` and `workflow/WORKFLOW.md`.
    - Added dedicated test coverage in `tests/test_sectors.py`. All 97 unit and GUI tests passing (exit code 0).
  - **Multi-PDF Annual Reporting Suite Linkage (IAR & AFS Architecture)**:
    - **User-Driven Document Classification & Toolbar Controls (`section_capture/window.py`, `section_capture/db.py`)**:
      - Supported canonical document roles: `IAR` (Integrated Annual Report), `AFS` (Annual Financial Statements), `PRES` (Results Presentation), `SENS` (Continuous Disclosure), and `AR` (Consolidated Annual Report).
      - Added `DocumentClassifyDialog`: Prompts user with keyboard-accessible modal on PDF open with heuristic pre-selection.
      - Added `doc_type_combo` directly on `doc_bar` toolbar for instant 1-click reclassification.
      - Updated `_refresh_document_selector()` with distinct badges: `[IAR]`, `[AFS]`, `[PRES]`, `[SENS]`.
    - **Companion Auto-Linking & Synchronized Questions Ledger (`section_capture/db.py`)**:
      - `auto_link_companion_reports()`: Automatically links sibling AFS / Presentation PDFs to the primary IAR via `parent_report_sha256`.
      - Bidirectional questions ledger synchronization: questions raised in the IAR immediately carry over to the AFS, and vice-versa.
    - **Document-Prefixed Evidence Captures & Citations (`section_capture/packages.py`)**:
      - Selections record `"doc_code": "IAR" / "AFS"` and `"source_filename"`.
      - Section headers format page citations unambiguously: `--- Section 05 | [AFS] physical page 24 | text selection | financial_note ---`.
      - Prompts instruct models to cite document roles: `Pending: [AFS Note 12 - Contract Assets on physical p. 42]`.
    - **Multi-Document Stage 1 Working Paper Compilation (`workflow/export_stage1.py`)**:
      - Automatically aggregates the complete suite into structured parts:
        - `PART 1: PRIMARY FINANCIAL DISCLOSURE (IAR)`
        - `PART 2: AFS FINANCIAL STATEMENTS & TECHNICAL NOTES`
        - `PART 3: SUBSEQUENT SENS ANNOUNCEMENTS`
    - Added comprehensive unit and GUI tests in `tests/test_multi_report.py`. All 101 tests passing (exit code 0).
  - **Sequential Batch Submissions & 'Run All Pending' (`workflow/resubmit_sections.py`, `section_capture/map_dialog.py`)**:
    - Upgraded `workflow/resubmit_sections.py` with `--report` selection and `--missing-only` resume mode, seamlessly threading the questions ledger across pending sections without wiping earlier responses.
    - Integrated a **`Run All Pending`** 1-click action in `SavedSectionsDialog`, executing automated sequential DeepSeek queries with real-time progress and error handling.
  - **Construction & Materials Sector Onboarding (`companies/sectors.py`, `prompts/construction/`)**:
    - Added canonical `construction` sector (`Construction & Materials`) to centralized `SECTOR_REGISTRY` with cyan color palette (`#ecfeff` / `#155e75` / `#a5f3fc`) and aliases (`materials`, `building`, `cement`, `infrastructure`, `engineering`).
    - Configured Stage 1 persona: `Managing Director and Senior Forensic Construction & Infrastructure Financial Auditor`.
    - Configured Stage 2 persona: `Managing Director & Head of Construction & Materials Equity Research`.
    - Authored `prompts/construction/00-report-orientation/v1.0.0/prompt.md` and `prompts/construction/12-analyst-reading-brief/v1.1.0/prompt.md` targeting:
      1. *Order Book Quality & Revenue Recognition (IFRS 15)*: Book-to-bill ratio, lump-sum vs cost-plus mix, percentage-of-completion, contract assets (unbilled WIP / accrued revenue), contract liabilities (customer advances), unapproved variation claims.
      2. *Materials Cost Inflation & Margins*: Building materials pass-through (CPAP / Haylett formula), aggregates/cement/bitumen pricing, quarry/kiln capacity utilization, plant/equipment fleet maintenance capex.
      3. *Working Capital & Retentions*: Retention receivables holdbacks (5-10%), trade receivables aging, municipal payment delays, and cash conversion ratios.
      4. *Onerous Contracts & Guarantees (IAS 37)*: Onerous contract provisions, performance/advance payment guarantees, bonding line headroom, and delay damages.
      5. *Balance Sheet & Covenants*: Net Debt to EBITDA, interest cover, and asset finance.
    - Added construction company mapping in `section_capture/db.py` (`WBO`/`WBHO`, `RBX`, `PPC`, `AFT`, `SSK`).
    - Updated `new_company.py` with construction parameters (book-to-bill, operating EBIT margin, materials inflation, cash conversion, ZAR reporting currency).
    - Added test coverage in `tests/test_sectors.py`. All 102 unit and GUI tests passing (exit code 0).
  - **Asynchronous Capture, DeepSeek FIFO Queue, Batch Pending Runner & Completed Checkmarks (`section_capture/window.py`)**:
    - **Decoupled Instant Local Save (`Save Section`)**:
      - Renamed `Save & copy prompt` to `Save Section` to clarify its purpose (instant local SQLite save without waiting for AI response).
      - Decoupled `save_button` and `save_and_run_button` from `not_busy` state, enabling analysts to rapidly capture and save multiple sections sequentially even while background model queries are in flight.
    - **FIFO Background DeepSeek Queue (`_query_queue`)**:
      - `queue_or_run_package()`: Enqueues section package IDs into a FIFO background queue.
      - Before dispatching each query, automatically refreshes the package's reading prompt from SQLite with the latest `questions_ledger`, ensuring sequential verification questions are passed down accurately.
    - **1-Click Batch Runner (`⚡ Run Pending (N)`)**:
      - Integrated directly on the main capture sidebar.
      - Displays real-time pending count (`⚡ Run Pending (N)`) or in-flight progress (`⚡ DeepSeek Running (N in queue)`).
      - Enqueues all un-analyzed sections in the active report in section order.
    - **Completed Section Checkmarks in Heading Dropdown (`HeadingComboBox`)**:
      - `_refresh_heading_options()` dynamically inspects SQLite and prefixes already-saved sections with `✓ ` (e.g. `✓ 01. Financial Review`).
      - `HeadingComboBox` handles raw/display tuples and automatically strips `✓ ` upon selection or text editing, ensuring section titles in SQLite and report maps remain clean.
    - **UI Layout Deduplication**:
      - Removed duplicated `Saved sections` and `Stored questions` sidebar buttons that were already present in the top toolbar.
      - Streamlined auxiliary row to `[⚡ Run Pending (N)] [Review Sections →] [Copy prompt]`, keeping prompt clipboard copying accessible with 1 click.
    - Added dedicated test coverage in `tests/test_capture.py`. All 104 unit and GUI tests passing (exit code 0).
  - **Removed Auto-Generated 'Cover / Overview' Sections (`section_capture/report_map.py`, `section_capture/window.py`)**:
    - Eliminated automatic insertion of dummy `{"title": "Cover / Overview", "start_page": 1}` in `build_manual_section_map()` when manual section outlines start at physical page $> 1$.
    - Filtered phantom `"Cover / Overview"` entries in `_refresh_heading_options()` in `section_capture/window.py` so only user-defined sections populate the dropdown.
    - Cleaned legacy report maps in `documents/analysis.sqlite` (Calgro AFS, ORN, APF, and iOCO), re-indexing section IDs contiguously starting at `D001` for the first user-defined section.
    - Updated `tests/test_report_map.py`. All 104 unit and GUI tests passing (exit code 0).
  - **Refined Footnote Superscript Detection in PDF Extraction (`section_capture/pdf_source.py`)**:
    - Fixed an issue where parenthetical continuation labels or subheadings in smaller font (such as `(continued)`) adjacent to larger headers were incorrectly decomposed into markdown superscripts (`([^co][^nt][^in][^ue][^d])`).
    - Restricted superscript tagging to genuine footnote markers (1–3 digits like `[^1]`, footnote symbols `*`, `†`, or single isolated letters), preserving multi-letter continuation words as clean text.
    - Added dedicated test in `tests/test_capture.py`. All 105 unit and GUI tests passing (exit code 0).
  - **Fixed Missing `copy`/`json` Imports in Background Query Dispatcher (`section_capture/window.py`)**:
    - Fixed a bug where `_start_query_for_package()` crashed silently with `NameError: name 'copy' is not defined` when `Save & Run DeepSeek` or `Run Pending` was invoked.
    - Added missing standard library imports (`copy`, `json`) and wrapped the query dispatcher in robust `try...except` error handling with user-facing alerts.

## Next steps

1. **Active Coverage Universe (5 Assets Tracked)**:
   - `PAN`: BUY | Target R43.50 | Ref R30.69 (+41.7% upside / +47.6% TSR) | Mining
   - `APF`: SELL | Target R0.42 | Ref R0.60 (-30.0% upside) | REIT
   - `ORN`: HOLD | Target R0.26 | Ref R0.28 (-8.5% upside) | Mining
   - `LEW`: HOLD | Target R84.50 | Ref R79.00 (+6.96% upside / +18.86% TSR) | Retail
   - `IOC`: BUY | Target R4.90 | Ref R3.96 (+23.7% upside / TSR) | IT
2. **Construction Sector Deployment**:
   - Ready to scaffold construction and materials companies (e.g. `python new_company.py WBO --sector construction --name "Wilson Bayly Holmes-Ovcon"` or `RBX` Raubex, `PPC` PPC Ltd, `AFT` Afrimat).


