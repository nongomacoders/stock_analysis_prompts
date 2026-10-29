# Working process

## Current analysis and evaluation flow

1. The user downloads original company PDFs into the company's source folders.
2. The app scans/maps sections; DeepSeek analyzes captured sections one at a time with the evolving question ledger.
3. DeepSeek performs Stage 1, then Stage 2 including the final valuation.
4. Gemini independently evaluates DeepSeek and proposes evidence-supported improvements and guardrails.
5. Codex independently evaluates Gemini against original evidence, identifying supported findings, missed errors, and errors introduced by the evaluator.

The user runs Gemini in Antigravity. Prepare its local evaluation prompt and evidence
pack; do not submit Gemini calls through OpenRouter. Preserve the returned Gemini
output for Codex's subsequent review.

Automatic capture now splits oversized sections without discarding remainder pages.
New automatic section prompts use persistent question records and validated ledger
deltas; legacy captures retain compatibility. See [WORKLOAD_RELIABILITY.md](../docs/WORKLOAD_RELIABILITY.md)
for coverage limits, evidence validation and the separate comparison-run fallback.

Every evaluation automatically follows [the mandatory independent evaluation record](../docs/STOCK_EVALUATION_FORMAT.md#1a-mandatory-independent-evaluation-record-automatic). Save versioned evidence, calculations, coverage, findings, revisions, and handoff records alongside company briefs; preserve original model outputs before corrections. No repeated user prompt is required when the evaluator has access to these project instructions. This is a repository instruction workflow, not an automatic Gemini API integration. An external Gemini conversation must load these instructions through its project context. `evaluate_stock.py` supplies preliminary checks, not a substitute for independent review. The current flow supersedes historical model assignments below.

## DeepSeek improvement objective

Section briefs now use a shared four-part reading task plus concise conditional
sector notes. Keep material facts/qualifications,useful arithmetic and evidence
questions;do not require a full forensic audit of every capture. Structured JSON
ledger semantics remain unchanged. See [SECTION_READING_PROMPT.md](../docs/SECTION_READING_PROMPT.md)
for assembly,paired-pilot measurements and remaining model errors.
The subsequent NTU source-order trial uses the refined common prompt with an empty
ledger and no paid repairs. Raw briefs with rejected ledger deltas remain available;
only validated deltas feed later ledger state. Report generation coverage separately
from ledger validation and financial correctness. See the same document for results.

The final goal is to make DeepSeek as robust as possible. Gemini reviews DeepSeek output and Codex reviews Gemini against original evidence; verified lessons feed back into stronger prompts, reusable guardrails and better questions in the evolving questions ledger. Trace failures to the earliest affected section or stage so later analyses ask for the right evidence and catch recurring errors earlier. Preserve original outputs and distinguish proposed improvements from implemented changes and demonstrated improvements.

Ledger improvements should turn verified review findings into specific evidence requests and reconciliation questions, carry unresolved material questions forward with `Pending: [section]`, and require evidence before closure. Review completion alone does not establish improved DeepSeek performance; assess that separately when a comparison run is authorized.

## Material-issue publication gate

Stage 1 must carry unresolved material findings into Stage 2. A target and recommendation are optional: new Stage 2/SENS outputs require explicit readiness evidence and numerical reconciliations. Material failures or unsupported dependencies produce **VALUATION WITHHELD - MATERIAL ISSUES UNRESOLVED**, with null valuation fields and a list of required corrections. Raw candidates and previous notes are preserved; withholding clears stale production metrics and suppresses dynamic ratings. READY is not independent financial validation. See [VALUATION_WITHHOLDING.md](../docs/VALUATION_WITHHOLDING.md) for the contract, legacy behavior and implementation limits.

## Stage reasoning policy

DeepSeek requests through the shared OpenRouter client are restricted to Fireworks
(`provider.only=["fireworks"]`, fallback disabled, supported parameters required).
The default model is the base `deepseek/deepseek-v4.1-flash-1017` slug. This applies
to section analysis and both stages; other model providers are not restricted by
this DeepSeek preference. Request metadata records the requested provider settings.
The provider change does not alter the stage reasoning/token policy below.
Optional presentation-section clustering has a separate request path and uses the
same Fireworks restriction. It groups slide titles/snippets; PDF text extraction
and subsequent page capture remain local.

Section capture, mapping and ticker lookups retain the fast client default (`reasoning.effort=none`, 16,384 maximum completion tokens unless overridden). Stage 1, Stage 2, Stage 2 SENS updates and `evaluate_stock.py --rerun` explicitly request `reasoning.effort=max`, a combined reasoning/final-answer ceiling of 65,536 tokens and a 900-second HTTP timeout. Stage diagnostic scripts use the same reasoning policy and allow timeout/token overrides. Policy constants live in `section_capture/openrouter.py`.

Previously the API client hard-coded `none` for every request, including both analysis stages. The new policy requests max through OpenRouter's documented reasoning parameter and requires providers that support the requested parameters; retries and nitro fallback retain the policy. Provider mapping and actual reasoning consumption can vary, so requested effort is not proof of an achieved effort level or financial accuracy. Higher ceilings are limits, not guaranteed consumption; slower responses and higher output-token costs are expected when more reasoning is used.

The client excludes raw reasoning from returned reports and refuses reasoning-only or completion-limit-truncated results. Successful GUI Stage 1/2/SENS runs and CLI reruns save a `.run.json` file alongside the Markdown note, containing generation/model identifiers, requested effort and token ceiling, finish reason, reported reasoning-token usage (null if not supplied), provider when returned, and token/cost statistics. These metadata files do not contain credentials or raw internal reasoning. Existing analyses are not automatically regenerated; compare a fresh run against the preserved NTU/Gemini/Codex evidence before claiming a quality improvement.

Reference: [OpenRouter reasoning controls](https://openrouter.ai/docs/guides/best-practices/reasoning-tokens). Request serialization, worker forwarding, retries, response completeness and GUI stage separation are verified with mocked API tests; no paid live valuation is part of the configuration change.

## Historical 3-Tier Architecture (implementation background)

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

## Sector & Company Onboarding

- **Onboard a new sector (< 2 min)**: Run `python new_sector.py <sector> --name "..." --short "..."` per [`docs/SECTOR_ONBOARDING.md`](../docs/SECTOR_ONBOARDING.md). Centralized in `companies/sectors.py`, automatically populating UI dropdowns, badge styles, and Stage 1/2 personas.
- **Scaffold a company hub**: Run `python new_company.py <TICKER> --sector <sector> --name "..."`. Initialized under `companies/<SECTOR>/<TICKER>/` (`sources/`, `models/`, `research/`, `briefs/`).

---

## Evidence integrity rules

- Original PDFs in `companies/<TICKER>/sources/` remain read-only; source SHA-256 is verified before every save.
- Credentials and API keys are stored externally and never committed, logged, or inspected.
- Physical PDF pages are numbered from 1; printed page labels are stored only when explicitly entered by the user.
- Area selections extract only characters fully inside the crop box and warn when boundaries cross text or when a region is image-only.
- Report map availability shows what other sections exist for later reading; it does not imply those sections have already been inspected or verified.
- Stage 1 determinations are the working baseline for Stage 2. Reopen contradictions against primary evidence and track resulting corrections; an audit label does not make a finding authoritative.
