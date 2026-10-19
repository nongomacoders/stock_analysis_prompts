# Working process

## Standardized 3-Tier Analysis Architecture

The repository operates a multi-tiered pipeline that completely eliminates narrative fluff and whole-PDF hallucinations while removing manual bespoke modeling code:

### Tier 1: Interactive Section Capture & Rapid Scrutiny (DeepSeek Flash 4.1)
1. **Scan major sections first**: Opening a company PDF in the local PySide6 app (`Run Capture.cmd` / `app.py`) scans native headings across all physical pages (`section_capture/report_map.py`) and initializes report metadata in the central SQLite database (`documents/analysis.sqlite`).
2. **Capture in sections**: Select text or area regions from the PDF (`section_capture/window.py`), assign explicit data types (`commentary`, `table`, `financial_note`), and attach targeted analyst queries.
3. **Programmatic OpenRouter query**: 
   - Clicking `"Save & Run DeepSeek"` saves the section package and asynchronously queries **DeepSeek Flash** (`deepseek/deepseek-v4.1-flash-1017`) via the user's OpenRouter API key (loaded in-memory from external secrets).
   - The model scrutinizes footnotes, identifies cross-section checks (`Pending: [section]`), and outputs an updated **Open Questions Ledger**.
   - The response is automatically stored in `sections.llm_response`, and Section 4 (`Updated Open Questions Ledger`) is parsed directly into `reports.questions_ledger` for the subsequent section.
   - Alternatively, `"Save & copy prompt"` remains available for manual clipboard workflows.

### Tier 2: Independent Cognitive Forensic Audit (Gemini 4 Argon — Stage 1)
1. **Compile full working paper**: Run `python workflow/export_stage1.py <TICKER>` to compile the chronological extraction dossier and evolving questions ledger across all captured sections into `companies/<TICKER>/briefs/<TICKER>_stage1_forensic_prompt.md`.
2. **Forensic reasoning only (No PDF attached)**: Gemini 4 Argon acts as Senior Forensic Mining Accounting Auditor to independently resolve core accounting and operational junctions:
   - Diluted share count and acquisition allotment recognition dates.
   - Balance sheet cash and gross debt de-gearing (Net Debt vs Net Cash).
   - Share-based payment (SBP) cash settlement accounting and underlying recurring EBITDA.
   - Third-party buy-in feedstock unit cost distortions on Group and asset AISC.
   - High-cost shaft identification (e.g. Sheba/Consort) and structural cost drag.
   - Capex trajectory: Uncommitted growth budgets vs technical sustaining capex cliffs.
   - South African Section 36 gold mining tax formula ($Y = 33 - 165/X$) and upfront capex shields.
3. **Save audit determinations**: Store Argon's verified response in `companies/<TICKER>/briefs/<TICKER>_stage1_audit_response.md`.

### Tier 3: Institutional 2-Year Forecast & JSE Equity Valuation (Gemini 4 Argon — Stage 2)
1. **Generate valuation prompt**: Run `python workflow/generate_stage2.py <TICKER>` to create `companies/<TICKER>/briefs/<TICKER>_stage2_valuation_prompt.md`.
2. **Audited ground truth + PDF execution**: Gemini 4 Argon acts as Head of Mining Equity Research, taking the attached company PDF report alongside the Stage 1 audited determinations as authoritative ground truth to formulate:
   - Asset-by-asset 2-year operational forecasts (throughput, grade, recovery, AISC).
   - Consolidated P&L and Free Cash Flow to Equity (FCFE) under Scenario A (Expedited Growth) and Scenario B (Committed Capex Cliff).
   - Sum-of-the-parts (SOTP) DCF and forward EV/EBITDA valuation.
   - Definitive 12-month JSE target price in **ZAR (Rands per share)**.

---

## Evidence integrity rules

- Original PDFs in `companies/<TICKER>/sources/` remain read-only; source SHA-256 is verified before every save.
- Credentials and API keys are stored externally and never committed, logged, or inspected.
- Physical PDF pages are numbered from 1; printed page labels are stored only when explicitly entered by the user.
- Area selections extract only characters fully inside the crop box and warn when boundaries cross text or when a region is image-only.
- Report map availability shows what other sections exist for later reading; it does not imply those sections have already been inspected or verified.
- Stage 1 determinations form strict ground truth for Stage 2 modeling; the model is prohibited from reverting to high-level PR narratives when audited reconciliations exist.
