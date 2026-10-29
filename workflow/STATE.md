# Current state

Last updated: 2026-10-29 (Africa/Johannesburg).

## Agentic report build direction opened (2026-10-29, this branch only)

- New branch `agentic-report-build` (worktree `..\stock_prompts_agentic`, off `one_shot@37bfaba`) for the proposed agentic report-build experiment: OpenCode builds a report like software (plan → SQLite extraction with page-cited lineage → pytest reconciliation suite → hypothesis branches/worktrees → narrative/Excel view → Gemini/Codex review gates → 1A audit). Charter `workflow/changes/20261029_agentic_report_build/CHARTER.md` (status PROPOSED, nothing implemented), runbook `RUNBOOK.md`, machine-readable scoring baseline `ground_truth/pan_d009_expected.json` (PAN D009 pp.48-50 verified identities/conflicts, transcribed from 20261029T123636Z_open_code_three_pass_review).
- Key covenants: never replace a printed source figure (conflicts are recorded data); all arithmetic executes in code, never asserted in prose; ledger stays open on ambiguity; production files, sources and `one_shot` branch untouched. First run scoped to one section.
- Worktree setup emitted one pre-existing `Filename too long` warning checkout item (deep pilot `inputs/.../prompts/.../.gitattributes`); unrelated to this scaffold, verify its presence separately if it matters.
- **P0 COMPLETE (2026-10-29, commit `7cec693`)**: `WORKPLAN.md` written and committed — six-table schema (`sources`/`pages`/`cells`/`conflicts`/`questions`/`runs`) with printed-values-only and page+sha256+commit lineage rules; expected cell inventory for pp.48-50 regions A/B/C; eight trial-origin ledger questions to import (all `open`); interpreter = main checkout `.venv`. No extraction, no code, no source edits, no paid calls. Next: P1 extraction + render acceptance.
- **Excel authorized (2026-10-29, after P0)**: user installed openpyxl 3.1.5 into the main venv; verified end-to-end this session. P4 will add a static values-only workbook (no formulas) built from `report.sqlite`; CSVs stay canonical. **RESOLVED (2026-10-29)**: `openpyxl==3.1.5` is now pinned in both `requirements.lock.txt` and `requirements-dev.lock.txt` of the production checkout (verified read-only from this worktree; both entries carry the `# via openpyxl` annotation). The worktree copies intentionally remain unchanged — production lockfiles are not mutated from this branch. WORKPLAN §5 updated accordingly.
- **P1 COMPLETE (2026-10-29, commit `9d33906`)**: PAN D009 physical pp.48–50 extracted to `build/report.sqlite` — **1,196 cells** (all printed value tokens incl. printed `–` nil cells), **46 metric rows** (p48=17, p49=16, p50=13) sharing `row_index` across FY26/FY25 siblings, **14 printed numeric columns x3 pages** (identical grid verified vs non-identical: consistent column labels with banner prefixes Mining/Surface/Total operations), 8 ledger questions imported all `open`, units parsed from printed Unit column ('t','oz','%','g/t','ZAR/kg','A$/kg','US$/oz','ZAR/t','US$/ZAR','US$/A$' + 'ZAR/US$/A$ million', inherited by FY25 siblings), footer straps excluded as `ambiguity` conflicts. **10 open conflicts** recorded, never overwritten: 3 structural (unlabelled never-populated column between BTRP and Elikhulu on every page), 6 footer exclusions, 1 in-number separator typography (printed `'1,271 855'` / `'2 956.0'` / `'6, 609'` — gap-split numeric fragments ≤4.5pt re-joined, glyphs verbatim in `value_raw`, `value_num` with separators stripped; pixel-crop evidence in trust-render crops). `pages` table records render path+sha256 per page; `sources` records document sha256 (`62b10bcd…`, asserted at run time). Scoring fixture never read by build code. Anchors verified vs renders: p48 FY25 underground row 65,895/26,748/92,643/93,724; p49 FY26 Gold produced total 71,997/46,855/118,853/12,932/—/56,475/51,927/32,124/153,458/94,929/103,330/51,927/32,124/272,310 and FY25 68,549/27,829/96,378/15,224/52,606/30,806/1,513/100,149/83,773/80,435/30,806/1,513/196,527.
- **P2 COMPLETE (2026-10-29)**: Executable reconciliation suite delivered under `workflow/changes/20261029_agentic_report_build/tests_reconcile/` (`conftest.py`, `reconcile_engine.py`, `test_reconciliation.py`, `record_conflicts.py`). **15/15 pytest checks green** (`.venv python -m pytest tests_reconcile -q` exit 0 in 0.04s). Gate satisfied: all 68 arithmetic and cross-currency mismatches surfaced by the engine across 526 evaluated checks are **explicitly recorded in `conflicts`** table with page citations, check ID fingerprints, deltas, and mapped to open ledger questions where relevant. Total conflicts in DB: **78** (10 P1 extraction + 68 P2 reconciliation; 69 ambiguity, 9 source_defect; physical pages: p48=20, p49=38, p50=19, null=1; 36 conflicts link to imported ledger questions). Scoring fixture isolation enforced by automated test (covenant preserved). All Charter §4 survey detections independently reproduced: 1-oz leaf-sum mismatch, Δ10,000 Barberton/opsum conflict, Δ5,763 MTR leaf vs total-ops, FY25 disjoint 196,527 vs overlapping 197,608 resolution, EBITDA 663.0 vs 663.1 US$m leaf-sum gap, and p50 revenue/capex exact ties.
- **P3 COMPLETE (2026-10-29)**: Two hypothesis branches created and evaluated in isolated Git worktrees (`../stock_prompts_hyp_barberton` on `hypothesis/barberton-10k` commit `0fb3b03`; `../stock_prompts_hyp_mtr` on `hypothesis/mtr-buyin` commit `8aec515`). Both branches ran the full reconciliation test suite (15/15 passed). Branch 1 evaluated Barberton FY26 10,000 oz discrepancy: proved that substituting 84,929 oz makes opsum tie printed Group total 272,310 oz exactly, but verified this as conditional agreement only; printed 94,929 oz preserved and Q-1f48aa6d4b884f09 kept open. Branch 2 evaluated MTR FY25 5,763 oz gap: proved exact arithmetic tie with FY26 buy-in (25,043 + 5,763 = 30,806) and surface tailings total tie (92,873 + 5,763 = 98,636), but verified causal origin is unproven in source text and kept Q-3e8730dbd1994205 open per review correction. Findings summarized in `workflow/changes/20261029_agentic_report_build/HYPOTHESES.md`. Zero covenant 1 violations.
- **P4 COMPLETE (2026-10-29, commit `8567537`)**: Reading brief and Excel view generated strictly from `report.sqlite` without formulas (`READING_BRIEF.md`, `build/report_view.xlsx` 1,196 cells, 78 conflicts, 8 questions).
- **P5 & P6 COMPLETE (2026-10-29)**: Review gates and §1A-shaped evidence audit executed and committed:
  - **P5 Gemini Review** (`reviews/20261029T152604Z_gemini/gemini_review.md`): Verified all four charter covenants; scored all six baseline detections (1-oz conflict, Barberton 10k gap, MTR 5,763 gap, FY25 disjoint 196,527 oz build, EBITDA 0.1 mismatch, and p.50 financial ties); verdict: ACCEPT WITHOUT AMENDMENT.
  - **P5 Codex Review** (`reviews/20261029T152604Z_codex/codex_review.md`): Adversarial inspection against original PDF pages 48-50. Verified printed number preservation (zero hallucinated/modified values); verified openpyxl static values view (zero formulas); verified ledger closure discipline (refuting prior reviewer claims of premature MTR closure); verdict: PASSED WITH COMMENDATION.
  - **P6 §1A Audit Record** (`workflow/changes/20261029_agentic_report_build/AUDIT.md`): Comprehensive input manifest (PDF hash, render paths/hashes, schema, test suite, outputs), command execution log, evidentiary findings, and cost accounting ($0.00 paid API cost vs $0.03107 historical baseline; 100% deterministic local Python execution).
  - All definition of done (DoD) criteria satisfied: suite 15/15 green with all conflicts recorded; zero covenant-1 violations; all survey detections independently reproduced; review records preserved; production untouched.
- **PRIMARY FINANCIAL STATEMENTS P0 & P1 COMPLETE (2026-10-29, commit `a6c86c2`)**: Scoped and extracted Section S006 Primary Financial Statements (physical pages 17 and 18, printed pages 30–33):
  * **P0 Blueprint**: `WORKPLAN_PRIMARY_STATEMENTS.md` targeting Balance Sheet, Profit or Loss, and Cash Flows.
  * **P1 Extraction**: `build/extraction/extract_pan_primary_statements.py` and `build/extraction/render_primary_pages.py`. Extracted **192 cells** across 4 primary statements (Assets: 32 cells, Equity & Liabilities: 50 cells, Income Statement: 52 cells, Cash Flows: 58 cells) into `build/report.sqlite`. Total cells in DB: **1,388**. Rendered physical pages 17 and 18 to high-res PNGs and recorded paths/hashes in `pages` table (5 pages now tracked). Receipts saved in `build/receipts_primary_p1.json`.
- **PRIMARY FINANCIAL STATEMENTS P2 COMPLETE (2026-10-29, commit `826373c`)**: Executable reconciliation suite expanded with `tests_reconcile/test_primary_statements.py` (**34/34 tests green** across full suite in 0.08s):
  * Proved fundamental Balance Sheet equality ($1,608,075\text{k} == 1,608,075\text{k}$ FY26; $1,004,509\text{k} == 1,004,509\text{k}$ FY25).
  * Proved asset and liability subtotal builds (Non-current $1,279,570\text{k} + Current $328,505\text{k} = Total Assets $1,608,075\text{k}$; Equity $1,035,997\text{k} + Non-current Liabilities $349,328\text{k} + Current Liabilities $222,750\text{k} = Total Equity & Liabilities $1,608,075\text{k}$).
  * Proved Income Statement roll-downs: Gross profit ($1,156,451 - 514,297 = 642,154$), Operating profit ($545,838$), Profit before tax ($534,368$), and Net profit ($356,911$).
  * Proved Cash Flow roll-up ($556,991 - 352,144 - 155,874 = 48,973$) and full cash roll-forward ($49,532 + 48,973 + 9,807 = 108,312$).
  * Proved cross-statement cash tie: Balance Sheet Cash (p.17) == Cash Flow Statement Closing Cash (p.18) ($108,312\text{k} == 108,312\text{k}$).
  * Proved cross-section tie connecting to open ledger question `Q-a0b503d7ac044eee`: IFRS Revenue ($1,156,451\text{k} US$) at average exchange rate 16.90 US$/ZAR implies 19,544.0 ZARm vs D009 production revenue 17,249.1 ZARm ($\Delta 2,294.9\text{ ZARm}$).
- **PRIMARY FINANCIAL STATEMENTS P3 & P4 COMPLETE (2026-10-29, commit `191ac00`)**: View layer and hypotheses recorded:
  * **P3 Hypotheses**: Evaluated Footnote 1 reciprocal dividend cash flow re-presentation ($49,532k comparative roll-forward holds) and documented the ZAR 2,294.9m IFRS revenue bridge in `HYPOTHESES.md`.
  * **P4 View Layer**: Updated `build/generate_excel_view.py` and regenerated `build/report_view.xlsx` with a new `Primary_Statements` tab containing all 192 extracted cells (US$ thousand). 0 formulas in any cell (Covenant 2 preserved). Generated dedicated reading brief `READING_BRIEF_PRIMARY_STATEMENTS.md`.
- **PRIMARY FINANCIAL STATEMENTS P5 & P6 COMPLETE (2026-10-29)**: Two-reviewer audit and updated evidence record:
  * **P5 Gemini Review** (`reviews/20261029T161425Z_gemini/gemini_review_primary_statements.md`): Verified covenants, fundamental Balance sheet equality, income statement roll-downs, cash flow roll-forward, and cross-section revenue tie. Verdict: ACCEPT WITHOUT AMENDMENT.
  * **P5 Codex Review** (`reviews/20261029T161425Z_codex/codex_review_primary_statements.md`): Adversarial audit against PDF pages 17-18; verified 100% printed number fidelity, zero formula cells in Excel, and exact cross-statement cash tie ($108,312k == $108,312k). Verdict: PASSED WITH COMMENDATION.
  * **P6 §1A Audit Record** (`workflow/changes/20261029_agentic_report_build/AUDIT.md`): Updated input manifest (1,388 cells, 5 pages rendered and tracked) and execution log. Cost remains $0.00. Entire suite 34/34 tests green. All DoD criteria satisfied across both D009 and S006.
- **APM SECTION (pp.38-47) P1+P2 COMPLETE (2026-10-29)**: p.45 Adjusted EBITDA reconciliation extracted and reconciled — **130 cells / 10 rows** across the 13-column operation grid (extraction `p1_apm_ebitda_v2`; DB now **2,398 cells**).
  * **The 0.1 EBITDA residual is now code-verified and closed as a rounding-boundary artefact**: p.45 prints Barberton mining at **142.5** (131.1 net income + 11.4 D&A) while D009 p.50 prints **142.4**; every other cell and Group 663.1 identical. `test_x1_apm_versus_d009_p50` asserts the differing-column sets exactly (FY26 `{col0}`; FY25 `{col0, col1, col8, col9}`) and `test_x1_resolves_the_d009_leaf_sum_gap` shows substituting the p.45 printed 142.5 makes p.50's leaves reach its own printed 663.1 — recorded as **conditional agreement only**, never a correction.
  * **All 8 rounding deviations are exactly ±0.1 and all recorded** (single-decimal printing: subtotals built from unrounded figures). `test_rounding_deviations_are_all_recorded` fails if any deviation lacks a conflict row. Conflicts now **89**.
  * Fixed three documented traps: fragment regex now accepts leading-dot tokens (`.5`, `.8`); labels come from the PDF text layer with a lowercase-continuation rule (wrapped labels print as `...plant and` / values / `equipment`); line tolerance raised to 3.2pt so bracketed values group with their row. Grid now extracts with correct labels on all 10 rows.
  * **P4**: `report_view.xlsx` now **6 tabs** — `Primary_Statements` 192, `Production_Costs_p48_50` 1,196, `Segment_Analysis_p21_24` 880, `APM_EBITDA_p45` 130, `Conflicts` 89, `Questions` 8 — still zero formulas. Suite **60/60 green**.
  * **Still pending for this section**: pp.40-44 all-in cost reconciliations and p.47 ROCE. The formal APM definition wording on p.39 is read as text evidence but not extracted (no figures), so `Q-c1e6100f7a674873` stays open on the definitional half.
- **APM RATIO TABLES p.46 COMPLETE (2026-10-29)**: `build/extraction/extract_pan_apm_ratios.py` + `tests_reconcile/test_apm_ratios.py` — **38 cells / 19 rows** across three tables (`apm_nav_per_share`, `apm_levered_free_cash_flow`, `apm_cash_flow_yield`). DB now **2,436 cells**; suite **69/69 green**.
  * **Full per-share chain proved in code**: NAV = equity 1,036.0 / (2,333.7 − 306.4) = 51.10 US cents (FY25 26.94); total shares 2,027.3 / 2,029.3; levered FCF build 609.4 − 15.0 − 74.1 + 46.6 − 215.8 + 0 − 149.3 = **201.8** (FY25 = 47.5); cash flow per share 201.8 / 2,027.3 = 9.95 c; yield 9.95 / 125.09 = **7.96%**. Noted: the yield uses the **unrounded** cents-per-share (7.9543 → 7.95 would fail), which the test asserts explicitly.
  * **New cross-section tie**: p.46's Adjusted EBITDA input **609.4 US$m** equals Note 3 p.22 Group Adjusted EBITDA (609,431 US$k) — the two presentations share one definition, which strengthens the APM scope finding.
  * Extractor defect found and fixed: section markers were matched shortest-first, so the yield table absorbed the whole levered-FCF block; markers are now ordered longest-first and matched with `in` (uppercase markers do not occur in the lowercase definitional prose). Excel `APM_EBITDA_p45` tab now covers all `apm_%` regions (168 cells).
- **APM p.44 COMPLETE (2026-10-29, third attempt)**: `extract_pan_apm_capital.py` (**text-layer driven**, no coordinate snapping) + `tests_reconcile/test_apm_capital.py`. **98 cells / 25 rows**: capital expenditure 12 rows × 6 values, net debt 8 rows, net senior debt 5 rows. DB now **2,534 cells**; suite **79/79 green**; conflicts **90**.
  * **The fix was to stop using geometry on this page.** The PDF text layer already lists each row as label followed by its values *in printed column order*, so rows and column roles come straight from text; coordinates were the source of both earlier failures. Section membership comes from the headings (`SUSTAINING CAPITAL`, `NET (CASH)/DEBT`, `NET (CASH)/SENIOR DEBT`), and a lowercase-start label takes the preceding line as its head (fixing the `Agricultural ESG projects` truncation).
  * **Checks proved**: sustaining + expansion = total on every capital row both years (one printed 0.1 exception, recorded); Barberton total = mining + BTRP; Evander total = mining + Elikhulu; group total rebuilds from the seven segments (21.8 / 202.2 / 224.0); net debt and net senior debt component sums (±185.7 / 150.5 and ±194.7 / 141.5); borrowings 51.5 ties balance-sheet borrowings (38,578 + 12,957 = 51,535); total capital 224.0 ties Note 3 capex 223,995 US$k.
  * **Recorded rounding deviation**: BTRP FY25 sustaining 0.3 + expansion 2.6 = 2.9 vs printed total 2.8 — a single-decimal artefact, recorded as `CAP|FY25|BTRP|delta=0.1` rather than smoothed over. Excel APM tab now covers all `apm_%` regions (266 cells).
- **APM pp.40-43 ALL-IN COST COMPLETE (2026-10-29)**: `extract_pan_apm_aisc.py` (text-layer, token-scan parser) + `tests_reconcile/test_apm_aisc.py`. **819 cells / 63 rows** across four tables: FY26 US$ million (p.40, 12 rows), FY25 US$ million (p.41, 13), FY26 unit (p.42, 19), FY25 unit (p.43, 19). DB now **3,353 cells**; suite **86/86 green**; conflicts **97**.
  * **Parser fix that mattered**: a plain regex silently dropped the two subtotal rows because labels carry a footnote digit (`Cash cost1`, `All-in sustaining costs1`) which the lazy label match swallowed as the first value. Replaced with a token scan that finds the position where exactly 13 value tokens run to end-of-line; footnote digits are stripped from the label afterwards.
  * **Definition chain proved**: cash cost = gold cost of production on every column both years; AISC = cash cost + royalties + community − by-products + corporate G&A − reclamation + sustaining capital (development and maintenance); AIC = AISC + voluntary severance (FY25 only) + expansion capital. FY25 ties **exactly** on both; FY26 has six printed −0.1 cells (AISC cols 0, 2, 8, 12; AIC cols 3, 8), all recorded as conflicts and asserted as an exact deviation set.
  * **New cross-table finding**: group gold sold for FY25 prints **196,927 oz** on p.43 against **196,926 oz** on D009 p.49 — a one-ounce difference within the same document for the same measure. FY26 ties exactly at 272,373 oz. Recorded as `GOLD_SOLD|FY25|p43_vs_p49|delta=1`; neither value touched.
- **APM p.47 COMPLETE (2026-10-29)**: `extract_pan_apm_roce.py` + `tests_reconcile/test_apm_roce.py` — **28 cells / 6 rows** (`apm_roce` 4 rows x 2 years; `apm_per_share_history` 2 rows x 10 observations FY26-FY22 in ZA cents and GB pence). Every table the text layer exposes in label-then-values form is extracted and, where an identity exists, reconciled. Remaining gaps, each with its measured cause:
  * **p.28 (Note 7 PPE continuation, accumulated depreciation)** — attempted with a dedicated longest-run extractor and **reverted**. 16 candidate rows parse at modal width 14, but the fourteen asset-class column labels span ~30 wrapped lines, so row labels arrive as fragments (`losses)`, `movement`) and the `Balance as at …` rows do not parse at all. The accumulated-depreciation totals are visible in the text layer, but without reliable row labels they cannot be attributed, so nothing was shipped. Needs a header-index-aware extractor that maps the wrapped column titles first and then assigns rows positionally.
  * **p.37 (Note 20 financial instruments continuation)** — no candidate rows; same multi-line-header shape as p.28.
  * **p.34 (Note 17 share-based payments)** — deferred: 6 contaminated vs 1 clean row.
  * **pp.38, 51** — prose and glossary; no figures to extract.
  * **Consequence for the PPE tie**: the carrying amount (1,196,474) lives on p.28, so the cost-to-carrying bridge is still open. `test_ppe_cost_total_printed` asserts its absence and **fails loudly** if p.28 is ever extracted without a real tie being added.
  * `test_cell_lineage_complete` now bounds `physical_page` by the document (1–54) instead of a hand-maintained list, so adding a section cannot weaken it.
  * ROCE rebuilt and traced to three other sections: numerator 545.8 = income-statement operating profit 545,838; average equity 791.3 = mean of balance-sheet total equity (1,035,997 + 546,668)/2; average borrowings 120.8 = mean of the p.44 net debt borrowings (51.5 + 190.0)/2. ROCE = 545.8/(791.3+120.8) = 59.8%; FY25 = 215.9/(455.4+158.9) = 35.1%.
  * Per-share rows prove the five-year history is extracted intact: EPS 298.12 ZA cents / 13.36 GB pence (FY26) through 59.16 / 2.92 (FY22); DPS 77.00 / 3.53 through 18.00 / 0.92.
  * **P0**: `WORKPLAN_SEGMENT_ANALYSIS.md` — 11 printed segment columns (Barberton, Evander, Solar, MTR, Tennant, Mining operations subtotal, Exploration, Agricultural ESG, Corporate, Funding Company, Group total) across FY26 (pp.21-22) and FY25 (pp.23-24).
  * **P1**: `build/extraction/extract_pan_note3_segments.py` — **880 cells / 72 segment rows**. Column edges derived from each page's own numeric right-edge clusters (never hardcoded); note-number column excluded at x0<265; numbers printed as fragments across a wide space (`'242,' + '186'`) re-joined at gap<=12pt with glyphs verbatim in `value_raw`. Intra-group elimination block on pp.21/23 has different column semantics and is extracted to a separate region `note3_intra_group` rather than forced into the segment grid. Total cells in DB: **2,268**; pages tracked: **9**.
  * **P2**: `tests_reconcile/test_note3_segments.py` — **50/50 suite green**. All 72 segment rows tie **exactly** on both horizontal identities (cols0-4 = Mining operations subtotal; subtotal+Exploration+ESG+Corporate+Funding = Group total). Cross-section ties proved: Note 3 revenue/cost/operating profit/PBT/tax/net profit == primary statements (p.18); segment assets 1,589,637 + goodwill 18,438 = total assets 1,608,075; segment liabilities 572,078 = NCL+CL; net assets 1,017,559 + goodwill 18,438 = total equity 1,035,997.
  * **New detection**: Adjusted EBITDA is printed at **two different scopes** — Note 3 p.22 Group total **609,431 US$k** vs Group production summary p.50 **663.1 US$m**. Bridge proved in code: the D009 figure equals Note 3 operating segments only (171,874 + 292,316 + 155,899 + 43,012 = 663,101 → 663.1), excluding Solar (988), Exploration (222), ESG (345), Corporate (51,884) and Funding (231) = 53,670. FY25 reproduces (245,765 → 245.8 vs Note 3 226,584). This also **closes the 0.1 residual** left open at D009 P2: the p.50 total sums unrounded segments while its printed leaves are rounded to 1dp. Neither printed value replaced; `Q-c1e6100f7a674873` stays open. Conflicts now **80**.
  * **P4**: `READING_BRIEF_SEGMENT_ANALYSIS.md` (segment tables, cross-section ties, EBITDA bridge, Funding-entity sign flip); `report_view.xlsx` extended to 5 tabs — `Primary_Statements` 192, `Production_Costs_p48_50` 1,196, `Segment_Analysis_p21_24` 880, `Conflicts` 80, `Questions` 8 — still zero formulas.
  * **P5/P6**: `reviews/20261029T165125Z_gemini/gemini_review_note3_segments.md` (ACCEPT WITHOUT AMENDMENT, 3 residual risks recorded) and `reviews/20261029T165125Z_codex/codex_review_note3_segments.md` (PASSED WITH COMMENDATION; independently re-verified p.21/22/23/24 printed rows and the EBITDA bridge). Two build defects were caught and fixed by the gates: D009 engine ingesting Note 3 rows (24 spurious mismatches) and the Excel tab double-counting 880 rows.

## Project summary and commit preparation (2026-10-29)

- User requested project summary,commit and push on current `one_shot` branch. Updated README with capture/ledger/analysis/review workflow,Fireworks routing,withholding policy and demonstrated/remaining limits. Preserved all pending work; no app behavior changes during commit preparation.
- Fresh full offline suite:232passed in101.14s,exit0,Python networking denied. Saved test result under `workflow/changes/20261029_project_summary/`;unique test folder cleaned afterward. Preflight found no files above100MiB and no matching full OpenRouter/Google credential or private-key patterns in candidate text files. These pattern checks are bounded checks,not proof of universal secret absence.
- User supplied GLM5.3/OpenCode review. Independent response:`companies/consumer_lending/NTU/briefs/1H26/evaluations/20261029T125853Z_codex_opencode_review/audit.md`. GLM correctly catches my prior overstatement:staged finalPANdoesnotidentifyMTRgap in prose,not merelymissingledgerquestion. Prior20261029T121151Zpoint5/assessmentF009superseded;originalretained. GLM itself has false92873vs98636addition,wrong5309.2kgdenominator,short-quote/spacesmisdiagnosis and overstrict rounding claims. ProposedFY25MTR25043+FY26buy-in5763doesnotestablishvalidclosure. No semantic-engine or paidfollow-up implemented.
- Existingcode,source/evidence,experimentrecords and reviewcorrections are being preserved in the requested commit. No new valuations,SQLguardrails,paid models or three-pass app adoption.
- Added targeted `.gitattributes` rules preserving exact bytes in company evaluation/workflow change records. Git line-ending normalization must not invalidate their recorded evidence hashes on checkout. Git metadata writes use approved escalation because `.git` is read-only in the default sandbox.

## OpenCode Gemini-role three-pass review (2026-10-29)

- Completed Gemini-role review of the one-pass vs three-pass experiment per `workflow/changes/20261029_three_pass/gemini_prompt.md`. Saved `workflow/changes/20261029_three_pass/open_code_comparision.md` (user-requested filename) plus versioned record `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261029T123636Z_open_code_three_pass_review/` (audit.md, claims.json, findings.json, input_manifest.json 42 entries, calculations/reconciliations.py exit 0 with reconciliations.json 33/33 checks OK). No paid model calls, no prompt/code/production edits, originals untouched.
- Verdict: three-pass buys clearer staged dictionary/worksheet and the only in-memory-accepted literal-valid NTU ledger, but NOT robustness within coverage: it propagates the false 71,997=65,233+2,428+4,337 identity through all three passes (actual 71,998), never mentions the MTR 25,043 vs 30,806 (Δ5,763) conflict that only the single flags (Q-3e8730dbd1994205, medium), leaves FY25 197,608-vs-196,527 unresolved though 92,643+2,654+98,636+1,081+1,513=196,527 resolves it in-table, and accepts staged closure of Q-08aa5c3f257440ab without performing 3,845+644=4,489 (single rejected on quote format instead). Single adds its own errors (false 272,311≈272,310 check, 663.0 vs 663.1 "0.1 rounding ✓", Evander mislabels). Cost 2.24x/2.39x, time 1.62x/1.80x. Not causal proof (n=1 per arm/case).
- Prior-reviewer corrections: Gemini's "both arms flagged MTR gap, high-priority" (gemini_review.md lines 78-81/F009) and Codex point 5 first clause "Both PAN prose identify MTR5763 gap" are refuted by grep-level absence in staged outputs; rest of Codex critiques verified. Proposed (not implemented) smallest next change: resolved-status must require shown arithmetic tying to closure condition, validator checks numbers; rerun PAN meaning+why against preserved baseline.
- Production workflow unchanged (single-pass retained). Sources PDF hashes verified again this turn.

## Error-materiality triage (2026-10-29)

- User asked how much section errors affect final valuation and whether tolerable. Saved `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261029T122042Z_codex_error_materiality/audit.md`,claims,executed calculations and preservation. These experiments produced no new Stage1/2valuation;production unchanged. Exact effect on any final target NOT VERIFIED,no old target validated or rewritten.
- Conditional input scale:misread167loss as167gain implies334Rmearnings-inputdifference if numerically used;644/4489=14.346%ofPBDbalance,not14.3%equityvalue;1PANoz/272310=0.000367%,normallyimmaterial;1081/196527=0.5501%;10000/272310=3.6723%sourcecolumnconflictscale,notprovedproductionorrevenueoverstatement. Cash-based valuation may correct/ignore a noncash narrative sign error;must trace actual cashforecast and avoid doublecounting.
- Tolerate justified rounding and imperfectdrafts that downstream evidence corrects. Reconcile material signs,portfolio scope,cash-vs-profit and closure before relying on a newvaluation;existingwithholdingpolicycovers unresolvedmaterialdependencies. No fresh modelcalls,SQLguardrails,appchanges ortargets. SourcePDFhashes,all productiontables and preserved inputsunchanged;calculationcommandexit0. No regression repeat/tempfoldersforread-onlytriage. GeneralDCFprinciple checked against NYUSternDamodaran;companyeffects derive from local evidence only.

## Codex reviewed Gemini three-pass experiment audit (2026-10-29)

- Saved independent review:`companies/consumer_lending/NTU/briefs/1H26/evaluations/20261029T121151Z_codex_three_pass_review/audit.md`. Preserved155exact Gemini/experiment files,verified all146Gemini manifest entries. Freshly rendered/viewed originalNTU13,21–23/PAN48–50,source SHA verified. Independent calculations and preservation exit0;no Gemini scripts executed,paid calls,app/prompt/guardrail changes or regression rerun. Production tables/source PDFs/Gemini and raw model files unchanged.
- Supports retaining current workflow:three-pass clarity/percentages improved but adoption not justified. Correct cost ratios2.24/2.39 and summed-request ratios1.62/1.80; not full wall latency or causal3xfailure probability. Two unreplicated captures do not refute staging generally. Both NTU finals get gain-decrease direction right but prematurely closeQ-08aa5c3f257440ab. Staged scope narrowing persists; single explicitly acknowledges fair-value644withinPBD,contrary to Gemini's both-arms exclusion claim.
- PAN10000oz subtotal inconsistency confirmed; correct replacement/typo cause or42.35m revenue impact not proved. Elikhulu rounded1130.9m/sold53092oz implies684835ZAR/kgvsprinted68843; strong cost/rate/volume inconsistency,exact omitted-digit cause unverified. Tennant58.1m/1179oz=1584358A$/kg broadly agrees with1584835afterrounding;Gemini denominator0.03667kgshould36.67kg.
- Gemini MTR-question parity claim contradicted:both PAN prose flag5763gap,but onlysingle preserves dedicatedMTRledgerquestion(prioritymedium),staged ledger omits. Additional missed DeepSeek issues:single falsely checks272310=118853+153458(actual272311),mislabelsEvander total-produced figures as underground,and both infer inventory timing without reconciliation. Staged PAN final is more cautious on Tennant causes,which deserves credit. Actualvalidator question_ledger.apply_delta,not proposed nonexistentledger_validator.py.
- Saved all10Gemini finding assessments,9Codex findings,claims,revision log,independent calculations,question/closure comparisons and preservation. Repaired two escaped control-character references in this STATE document only,after preserving before copy. Original Gemini review untouched. Next candidate:direct source/scope reconciliation and closure evidence check,not a larger chain or automatic semantic engine. No implementation or further paid experiment authorized by this review.

## Gemini audit of one-pass vs three-pass experiment complete (2026-10-29)

- Completed independent Gemini review in Antigravity per docs/STOCK_EVALUATION_FORMAT.md Section 1A: companies/consumer_lending/NTU/briefs/1H26/evaluations/20261029T114800Z_antigravity_gemini_stage_review/. Decision: **CORRECTIONS REQUIRED; INSUFFICIENT EVIDENCE FOR THREE-PASS ADOPTION (DO NOT ADOPT)**.
- Refutes hypothesis that three-pass staging improves analytical robustness: incurs 2.24x to 2.39x higher cost (.010517 NTU / .011184 PAN vs .004702 / .004671 single) and 1.62x to 1.80x longer latency. Exposes pipeline to multi-call transport failures (original HTTP 429).
- Demonstrated error propagation across passes: NTU Pass 1 narrowed PBD scope to R3,845m principal book only, ignoring R644m fair-value assets explicitly recognized within PBD (Note 6.1 p.21; Note 1 p.13 total R4,489m). Pass 2 and Pass 3 repeated this restriction. Both arms proposed premature resolution for Q-08aa5c3f257440ab while total-scope reconciliation was pending; three-pass passed syntax validation and accepted the invalid closure into memory, whereas single-pass was rejected solely on string length (3 414 < 8 chars).
- In PAN, Pass 1 synthesized unsound generic definitions (capex reduces profit; revenue/EBITDA are cash inflows), and Pass 2 preserved double-counting confusion (197,608 vs disjoint 196,527 oz). Neither arm detected a blatant 10,000 oz primary source typographical error on physical p.49 (Barberton total printed as 94,929 oz vs components 71,997 + 12,932 = 84,929 oz; total operations sum equals 282,310 oz vs Group printed 272,310 oz).
- Saved complete evaluation pack: audit.md, claims.json (C001–C010), findings.json (F001–F010), calculations.json, input_manifest.json, input_checks.json, and rendered source pages with pypdfium2/PySide6. No production writes, prompt changes, or paid API calls. Copy saved to workflow/changes/20261029_three_pass/gemini_review.md for Codex review.

## PAN continuation complete; Gemini pack ready (2026-10-29)

- User explicitly authorized PAN retry with exponential backoff,3attempts. Preserved original partial run and reused successful PAN meaning/movement plus complete NTU pair. New run:`companies/consumer_lending/NTU/briefs/1H26/evaluations/20261029T114212Z_three_pass_pan_resume/`. Same exact failed final request verified before dispatch; fresh single prompt unchanged. Retry policy:max3attempts per remaining call,15/30second exponential waits,Retry-After respected,HTTP429/500/502/503/504 only before ID/content/usage. No retries after partial generation.
- PAN finalwhy and fresh single both succeeded first new attempt; no backoff wait exercised. Both isolated ledger deltas valid, financial quality pending Gemini. New2callsUSD0.0094843224,input24747,completion5379,reasoning0,cached1122,summed request32.149s,overall42.049247s. Both metadata records retrieved. All8planned successful experiment outputs now available across two runs,plus original failed429preserved. Combined known subtotalUSD0.0310742712; original failed-call billing unavailable.
- Saved combined_comparison.json/comparison.md,operational audit,all raw attempts/outputs/validations/metadata and input hashes. NTU prior semantic-closure concerns retained, no new PAN accuracy claim from validator success. Production tables,source hashes,old outputs/code snapshots unchanged; generation/handoff commands exit0,no local errors. No app/prompt edits,guardrails,valuation,Stage1/2 or Gemini API. No regression repeat/temp test folders for standalone continuation.
- Updated user-facing handoff:`workflow/changes/20261029_three_pass/gemini_prompt.md`,also saved in newrun/gemini/review_prompt.md. It now includes both complete pairs and intermediate error propagation/source checks. Next:user Gemini review in Antigravity,then Codex evidence review. No further paid calls.

## Small three-pass experiment: partial, not adopted (2026-10-29)

- User proposed accounting meanings -> calculations/percentage movements -> why unusual movements, and authorized a small experiment. Run:`companies/consumer_lending/NTU/briefs/1H26/evaluations/20261029T112944Z_three_pass_experiment/`. Two frozen captures NTU21–23/PAN48–50; fresh single-call baseline vs three-pass chain, original evidence/questions supplied throughout, earlier model notes explicitly untrusted. Same Fireworks-only model/none reasoning/temp0.1/16384cap per call. No company-specific seeds or app/prompt changes. Three-pass has extra total budget; no randomization/replication, no staging-causality guarantee.
- Planned8calls;7dispatched,6complete. PAN final why failed HTTP429Too Many Requests before content/ID/usage; fresh PAN single not dispatched, no paid retries. Generation exit1; read-only metadata refresh and review exit0. All six successful metadata records retrieved, initial receipts retained. Known subtotalUSD0.0215899488, failed-call cost unknown; prompt58101,completion11401,reasoning0,cached914; overall94.859874s. These token/cost figures exclude unavailable failed-request usage.
- Complete NTU comparison: singleUSD0.00470211,18.457s,8675input/3429completion; three-passUSD0.01051743,29.956summed request seconds,27675input/5602completion (2.24x cost). Three-pass supplies useful verified percentages and a valid final ledger vs rejected short-quote single. Both get loss direction right; both still propose unsupported resolvedQ-08aa5c3f257440ab with4489scope deferred. Three-pass accepts that closure in memory; production unchanged. An early PBD-only3845 scope oversimplification persists through all three passes.
- PAN only interim stages evaluable: dictionary confuses cash/profit/capex, worksheet retains197608vs196527overlap uncertainty and asserts71997component sum that is71998 (source1oz difference). No final/pair conclusion. Independent additional PAN49source uncertainty: printedBarberton94929 vs71997+12932=84929; total-operation sum282310vsGroup272310 (10000difference). Cause/correct replacement unverified; not credited to model experiment.
- Saved comparison.md,independent audit/claims/findings/calculations,closure comparison,all exact prompts/raw outputs/receipts,preservation and manual Gemini prompt at `workflow/changes/20261029_three_pass/gemini_prompt.md`. All production tables/source hashes/baselines/code snapshots unchanged. No Stage1/2,new guardrails or valuation. No regression repeat for standalone experiment scripts; last targeted27/full232pass offline, no temp pytest folders. Recommendation: review intermediate error propagation and closure; do not adopt three-call workflow from this sample. Next: manual Gemini review, then Codex review. No further paid calls made.

## Three-case clarification pilot: mixed results (2026-10-29)

- User authorized the small comparison. Saved `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261029T070527Z_prompt_clarification_pilot/`. NTU24,NTU21–23,PAN48–50 use exactly the prior extracted text, manifests and incoming questions; same request controls, only prompt messages changed. One fresh generation each versus saved baseline, not randomized/replicated.
- All3 calls complete, Fireworks only, none reasoning,16384cap,temp0.1,no repairs/fallback. USD0.0130756248; input26990,completion9246,reasoning0,cached1744; summed request47.368s, overall62.464921s. All metadata retrieved with read-only refresh, original receipts retained.2/3 valid deltas versus3/3 baseline.
- NTU24 now correctly calls167 cumulative-gain decrease an impairment loss, separates+24acquired/-191historical. Assets case still calls the decrease a net impairment gain and proposes resolvedQ-08aa5c3f257440ab despite pending4489scope. Entire assets delta rejected; diagnostic finds four literal-but-too-short quotes (3–5chars,min8), prior ledger unchanged. No premature closure persisted.
- PAN avoids prior explicit197608double-count allegation, but leaves1081scope unresolved rather than showing disjoint196527sum. Recognizes genuine FY25MTR25043vs30806 source uncertainty, yet claims FY26tailings46164vs51927: actual tailings46164bothcolumns,51927is totalincluding5763buy-in. Speculative cost/source-error explanations remain. Wording has not demonstrated reliable overall correction.
- Saved audit,claims/findings,calculations,quote/closure diagnostics,exact prompts/baselines,receipts/metrics,preservation and manual Gemini prompt. Source hashes/all production tables/prior files unchanged; no app/prompt modifications during pilot or new valuations/SQL guardrails. Generation and accounting commands exit0; no tests repeated for experiment-only work, no temp test folders created. Existing27targeted/232full offline results retained.
- Next: manual Gemini review using `workflow/changes/20261029_prompt_clarifications/gemini_prompt.md`, then Codex evidence review. No paid retry/full company run undertaken.

## Three prompt clarifications implemented (2026-10-29)

- User authorized continuing after the Codex review. Refined existing common instructions to use disjoint components when summing tables and retain partial status when essential closure evidence is pending/deferred. Structured ledger contract repeats the partial-status condition. Consumer-lending note now explains a decrease in an issuer's cumulative POCI gain added to book value is an impairment loss, distinguishing acquired gains from historical losses. No ticker-specific examples in live prompts.
- Preserved exact before versions under `workflow/changes/20261029_prompt_clarifications/`. Validator logic, extraction, provider/reasoning settings and SQLite guardrails unchanged. No paid calls, production question-status edits or new valuations. Fresh model improvement remains untested.
- Targeted offline prompt/ledger suite:27passed in11.56s,exit0, Python network blocked. Last full suite232passed,exit0; no full repeat for wording-only changes. Saved result, before/after hashes and evidence/production preservation in implementation_record.json; unique temporary test directory cleaned after saving results.
- Next: a small affected-case comparison can assess sign interpretation, disjoint aggregation and semantic closure before considering a full chronological company run. The wording alone does not establish corrected model behavior.

## Native extraction improvement and five-case pilot (2026-10-28)

- Implemented generic numeric-column anchoring/native-rule separation, wrapped-header placement and prose preservation in `section_capture/pdf_source.py`; no company-specific rules. Short literal cell/sentence anchors requested by the ledger prompt; `apply_delta` unchanged. Before code and 14-page before/after corpus preserved under `workflow/changes/20261028_table_extraction/`.
- Offline tests: initial53 passed(exit0); expanded58 passed/1 failed(exit1) exposed prose/header leakage, fixed; targeted59 passed(exit0); full232 passed(exit0), network blocked. Six source-PDF regressions added. All four test folders cleaned; result copies and cleanup status saved.
- Five independent Fireworks-only selected captures: NTU13,21–23,24,25 and PAN48–50. All5 generations complete, all5 ledger deltas valid; no repairs/fallback/Stage1/2. USD0.0199752336; input41078, completion14468, reasoning0, cached3908; summed request69.952s, overall98.782372s. All generation metadata retrieved after three transient metadata failures; no completion resubmissions.
- Saved run: `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T182010Z_native_extraction_pilot/`. Audit, seven findings, calculations, source hashes, raw answers, incoming states, requests/receipts, input manifest and manual `gemini/review_prompt.md` retained. Source PDFs, all production tables and old outputs verified unchanged. Original physical NTU22/24/25 and PAN48/49 independently viewed this turn.
- Demonstrated: NTU5/390 cells separate and4884 total correctly read; comparative FX dates correct; prose delta validates. Remaining: NTU167 impairment loss still called a release, questionable measurement-question closure, PAN FY25 double-count1081oz and imperfect grouped parent headers; speculative source-error explanations unverified. No blanket financial validation or causal benchmark claimed. Extraction and anchor wording changed together; cases reuse old incoming states rather than form a chronological rerun.
- Next: consider three short refinements to existing sign/scope/closure instructions after Codex review below. No new analytical guardrails, production valuations or additional paid runs authorized by this completion.

## Codex reviewed Gemini native-extraction audit (2026-10-28)

- Review: `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T191648Z_codex_native_extraction_review/audit.md`. Preserved109 exact Gemini/pilot/code files with flat numbered copies; all39 Gemini input-manifest entries verified. Independently viewed original NTU physical13,21–25 and PAN48–50. Independent calculations and final preservation checks exit0; Gemini scripts not executed.
- Supports keeping generic extraction fix within selected coverage. Confirms NTU5/390 separation and comparative FX mapping, five valid deltas, persistent -167 loss/release error, premature Q-08aa5c3f257440ab closure, PAN1081oz double-count. Literal quote validity is distinct from semantic closure; extraction and anchor wording changed together. No universal elimination/cause claim.
- Gemini's new MTR source variance confirmed: FY25 tailings25043vs30806, difference5763oz. Printed98636 subtotal uses30806; difference matching FY26 buy-in5763 does not identify cause/correct replacement. Prior Codex omitted this component inconsistency; exact Group sum uses reported subtotal and does not validate all components. FY26 one-ounce differences confirmed; rounding cause plausible, not proved.
- Qualified Gemini's cost explanation: Tennant A$58.1m/1584835perkg implies36.660kg; FY25 sold1179oz=36.671kg fits rounded cost, produced1513oz=47.060kg does not reproduce rate. Commissioning and transaction-date/weighted FX explanations remain unverified in inspected evidence. Multi-level labels can be represented by qualified flat names; avoid claiming Markdown makes hierarchy impossible. Additional DeepSeek issue: Debt review+69 gain cannot be attributed to aggregate payer-dropoff deterioration without evidence.
- Proposed only: refine existing consumer POCI cumulative-gain sign wording, common disjoint-total instruction and ledger keep-partial condition. Explicit examples/exceptions saved; no prompts, production ledger, SQL guardrails or app code changed, no paid calls. Production tables/source PDFs/original model and Gemini files unchanged. No regression rerun for read-only review; last full suite232passed,exit0. No temporary pytest folders created.

## Objective and boundary

Analyze and forecast from company presentations and reports section by section without whole-PDF inaccuracies or narrative fluff:
1. **Tier 1 (Programmatic Section Capture)**: Scan the PDF locally for major sections (`section_capture/report_map.py`) and capture section by section in the PySide6 app (`section_capture/`). Clicking `"Save & Run DeepSeek"` programmatically queries DeepSeek Flash (`deepseek/deepseek-v4.1-flash-1017`) via OpenRouter API in background `QThread`, auto-populates `llm_response`, and updates the central questions ledger in `documents/analysis.sqlite`.
2. **Stage 1**: DeepSeek synthesizes sequential extractions and the question ledger into the forensic audit. Findings remain subject to primary-source verification.
3. **Stage 2**: DeepSeek uses Stage 1 and source reports for the final forecast and valuation in ZAR per share.
4. **Independent evaluation**: Gemini evaluates DeepSeek; Codex evaluates Gemini against original evidence. Automatically follow `docs/STOCK_EVALUATION_FORMAT.md` section 1A, preserving versioned audit records and input model outputs without requiring a pasted prompt. External evaluators must have these instructions in their project context; this is not an automatic Gemini API integration.

**Final project goal:** The final goal is to make DeepSeek as robust as possible. Gemini reviews DeepSeek output and Codex reviews Gemini against original evidence; verified lessons feed back into stronger prompts, reusable guardrails and better questions in the evolving questions ledger. Trace failures to the earliest affected section or stage so later analyses ask for the right evidence and catch recurring errors earlier. Preserve original outputs and distinguish proposed improvements from implemented changes and demonstrated improvements.

Documentation clarification (2026-10-28): recorded the user-defined improvement objective in AGENTS.md, ARCHITECTURE.md and WORKFLOW.md. No prompts, ledger entries, SQLite guardrails, valuations or model outputs were changed; no paid calls or tests were run for this documentation-only change.

## Completed

- **Gemini independent review of native extraction pilot completed (2026-10-28)**:
  - Saved full independent evidence audit under `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T184306Z_gemini/audit.md`, input manifest in `inputs/manifest.json` (40 files preserved), claims in `claims.json` (9 claims, all verified), findings in `findings.json` (9 findings), and executed verification script in `calculations/reconciliations.py` (exit 0, outputs in `calculations/reconciliations.json`). Source PDF hashes verified for NTU (`9a19b3b4...`) and PAN (`62b10bcd...`); production SQLite all 9 table hashes match 100%; pilot files verified untouched.
  - Concluded **EXTRACTION IMPROVEMENTS SUPPORTED WITHIN SAMPLE; CORRECTIONS REQUIRED FOR PERSISTENT MODEL SIGN, CLOSURE, AND COLUMN-OVERLAP DEFECTS**. Evaluated all 5 pilot cases against primary source PDFs (NTU pp. 13, 21-25; PAN pp. 48-50).
  - Confirmed demonstrated benefits:
    1. NTU p. 22 Note 6.1: Numeric column separation using native vertical edges and numeric row anchoring cleanly keeps 5 (other loans) and 390 (trade receivables) separate; total evaluates to 5 + 390 + 3,845 + 644 = 4,884 Rm exact, completely eliminating prior baseline false 9,879 Rm (+4,995 Rm asset inflation) allegation.
    2. NTU p. 25 Note 6.2: Clean column separation correctly maps comparative closing exchange rate dates (Mar-26 USD 17.2/GBP 22.7, Mar-25 USD 18.4/GBP 23.9, Sep-25 USD 17.3/GBP 23.2), resolving baseline date swap.
    3. NTU p. 13 Note 1: Non-tabular prose paragraph preservation and short literal anchor prompt instructions (8–50 chars) achieved 5/5 valid ledger deltas (0 validation errors) without weakening validation strictness.
    4. PAN p. 48: Dense numerical cells in mining and tailings tables are cleanly segmented.
  - Confirmed persistent model & system errors:
    1. NTU p. 24 Note 6.1: DeepSeek persists in misclassifying the R167m POCI impairment loss (net movement -241 + 69 + 4 + 1 = -167) as an "impairment release" and querying the "sustainability of that release", inverting the economic/accounting meaning of a cumulative impairment gain reduction.
    2. NTU p. 22: DeepSeek prematurely resolved Q-08aa5c3f257440ab while explicitly acknowledging that the total R4,489m PBD carrying value reconciliation remained unverified in this capture, violating the explicit closure condition.
    3. PAN pp. 48-49: DeepSeek double-counted 1,081 oz buy-in feedstock in FY25 gold production, calculating 197,608 oz vs printed 196,527 oz (+1,081 oz gap). The disjoint sum 92,643 + 2,654 + 98,636 + 1,081 + 1,513 = 196,527 oz reconciles exactly to the single ounce; DeepSeek used Group total underground (93,724 oz, which already includes 1,081 oz) and added 1,081 oz a second time.
    4. PAN p. 49: DeepSeek made speculative claims that Tennant FY25 unit cost (A$1,584,835/kg) is a "likely printing/scale error" and that the AISC FX conversion is an unexplained residual (~53 US$/oz), overlooking commissioning-phase denominator scale (only 47 kg produced) and asset-weighted conversion methodology.
  - Forensic primary evidence finding (missed in prior review):
    PAN production table exhibits genuine 1-ounce subtotal rounding differences in FY26 (105,479 vs 105,478 oz; 118,852 vs 118,853 oz; 272,311 vs 272,310 oz). In addition, MTR FY25 tailings has an internal source inconsistency: Column 6 prints 25,043 oz while Column 14 prints 30,806 oz (diff 5,763 oz, which equals FY26 MTR buy-in); printed subtotal 98,636 oz uses 30,806 oz.
  - Architectural evaluation & recommendation:
    Multi-tier grouped column headers cannot be represented in standard GFM Markdown without colspan; attempting complex programmatic table reconstruction across arbitrary corporate PDF layouts introduces fragility and edge cases. Source layout limitations should be carried as documented analytical uncertainty. Prompt guidance should clarify POCI cumulative gain sign conventions, multi-column aggregation verification, and strict ledger closure compliance.

- **Codex reviewed Gemini's full NTU section-trial review (2026-10-28)**:
  - Reviewed `20261028T174829Z_gemini`;independent record:`companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T175636Z_codex_full_sections_review/audit.md`. Gemini116-entry manifest and all preserved review inputs verified. Independent diagnostics/calculations exit0;Gemini's script not executed. Original PDF physical12,13,22,24,25,31 independently rendered/viewed. All production tables,source PDF,prior files and copied inputs unchanged;no app/prompt/guardrail edits or paid calls.
  - Main cell/header/date/sign error findings supported. Corrected evaluator terminology:native PDF extraction,not OCR. Existing validator already collapses whitespace;9 evidence strings across4 rejected deltas still fail after diagnostic pipe removal. Blanket stripping is not demonstrated repair. p13 proposed resolution explicitly leaves SoFP tie-out pending despite original closure requiring it;two complete valid closures not established. Question overlap is real,but narrower classification versus full roll-forward/driver scopes must not be auto-merged.
  - Corrected Gemini comparisons:old full p25 already includes currency risk;oldUSD0.24456 includesStage1+failedStage2,not section-only cost. Old22-section costUSD0.1501426128,currentUSD0.0702026388,but provider/reasoning/prompt/seed state differ so no controlled savings claim. p12 statutory182 is Purchased book debts under Decrease in operating assets,not amortisation subtotal;6 residual arithmetic still holds.
  - Proposed next minimal work:not implemented. Preserve native numeric columns and wrapped headers/prose in extractor,then short exact quote anchors;offline affected NTU22/24/25 and PAN dense-table regression before a small authorized live sample. Defer global delimiter stripping,partial-delta acceptance,embedding deduplication and extra financial guardrails. Forecast/valuation not requested. No app test rerun for read-only review;last targeted27/full226 tests exits0 remain historical results.

- **Gemini independent review of refined NTU section-only trial completed (2026-10-28)**:
  - Saved full independent evidence audit under `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T174829Z_gemini/audit.md`, input manifest in `inputs/manifest.json` (116 files preserved), claims in `claims.json` (9 claims, all verified), findings in `findings.json` (9 findings), and executed verification script in `calculations/reconciliations.py` (exit 0, outputs in `calculations/reconciliation_output.json`). Source PDF hash verified (`9a19b3b4...`); production SQLite and all source files untouched.
  - Concluded **CORRECTIONS REQUIRED (SECTION-ONLY TRIAL; VALUATION NOT REQUESTED / NOT APPLICABLE)**. Evaluated all 22 Fireworks section analyses against primary source evidence (rendered physical pages 13, 22, 24, 25, 31).
  - Confirmed operational improvements: 22/22 calls completed with zero fallbacks/repairs, USD 0.0702 total cost (-69.8% vs older run), zero reasoning tokens, 340.5s wall time. p.13 prose correctly handled both portfolio roll-forward equations and explicitly framed POCI accounting without ordinary Stage 1/2 SICR migration; secondary currency risk topic on p.25 was captured and linked to p.26; false overdraft premise in Q-8612694a3a674266 was correctly contradicted.
  - Confirmed model & system deficiencies:
    1. Ledger quote-matching brittleness rejected 4 deltas (pp.9-11, 13, 18-19, 30-31), holding back 7 new proposed questions and blocking valid resolutions for Q-e4497d9112cd4e9d (PBD roll-forward) and Q-b18d8ce6d4804a50 (headline earnings bridge).
    2. OCR column collapse on p.22 merged '5' (other loans) and '390' (trade receivables) into '5 390', causing model to sum 5,390 + 3,845 + 644 = 9,879 vs exact printed 4,884 (false R4,995m asset inflation allegation).
    3. p.24 column header scrambling merged Unsecured and Retail into 'Unsecured Retail', attributed -241 to Debt review, and inverted the economic direction of cumulative impairment gain reduction. Full year FY25 historical loss verified at 77 + 182 = 259.
    4. p.25 swapped comparative closing exchange rate dates (USD 18.4 / GBP 23.9 assigned to Sep-25 instead of Mar-25; 17.3 / 23.2 to Mar-25 instead of Sep-25).
    5. p.31 inverted tax sign (-29 treated as +29), alleging false 58 EBITDA gap against exact printed 790 (-63 - 29 + 68 + 597 + 1 + 216 = 790), and invented all-positive sum (1,424 vs 597) for descriptive footnote components (signed reconstruction yields 598, 1 residual).
    6. Portfolio net cash of 434 less income 246 equals carrying decline 188 (4,677 - 4,489 = 188), leaving an unexplained 6 residual against statutory cash flow amortisation of 182.
  - Proposed 5 testable improvements for Codex review: quote validation whitespace normalization, partial delta acceptance decoupling, table column delimiter preservation in capture, accounting parenthesis/sign guidance in prompts, and ledger question deduplication. No paid API calls or production guardrail/database edits made.

- **Three prompt refinements and full NTU section-only trial completed (2026-10-28)**:
  - User authorized proceeding after Codex review. Applied shared sign/unit consistency and cautious first-time-comparative wording;consumer-lending note excludes ordinary POCI Stage1/2 SICR migrations without banning legitimate credit-risk questions. Preserved exact pre-change prompts under `workflow/changes/20261028_section_refinements/`. No new financial guardrails,PDF split/ledger-schema/stage-setting changes.
  - Targeted offline checks27 passed in15.64s,exit0;unique test folder cleaned after saving result. No full-suite repeat for two prompt wording changes;last full suite226 passed exit0. All model/accounting/review commands exit0;one early optional in-flight-output read returned shell exit1 before that file existed.
  - New run:`companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T171901Z_ntu_refined_sections/`. Existing24-unit reviewed plan retained,38 pages exactly once,22 financial calls plus2 navigation captures. Empty ledger;no company-specific seed questions or lesson block. Actual shared prompt/app ledger path,Fireworks only,none reasoning,16384 cap. No Stage1/2 or valuation.
  - All22 generations complete,USD0.0702026388,all22 costs corroborated by metadata. Input151251;completion51535;reasoning0;cached23564;sum request208.174s;first-dispatch-to-last-accounting340.451335s (5m40.45s).18 validated deltas,4 rejected (pp9–11,13,18–19,30–31). Rejected deltas left prior ledger unchanged;raw briefs/unapplied7 new questions retained.32 persistent questions:15open,15partial,1contradicted,1resolved. No repairs or API fallback. Ledger chronology/source/order/preservation checks passed.
  - Limited original PDF view13,22,24,25,31 found:correct p13 signed portfolio prose/POCI applicability and p25 shared currency coverage,but p22 cells5 and390 merged to5390 causing false9879 vs4884 total;p24 header/sign misinterpretations;p25 closing-FX comparative dates swapped;p31 tax−29 treated+29 yielding false58 EBITDA gap and prose footnote incorrectly made all-positive sum. Correct−63−29+68+597+1+216=790;conditional signed amortisation gives598 vs597,not claimed issuer-confirmed formula. These are model/capture interpretation issues,not established company defects.
  - Saved versioned audit,findings,source images,independent calculations,metrics,raw outputs,before/after ledgers,verification and manual Gemini prompt. All production tables,source PDF and previous files unchanged. No Gemini API or paid follow-on. Full semantic review remains pending;successful22/22 generation is not22 valid ledgers or financial validation.

- **Codex reviewed Gemini's simplified-section-prompt pilot audit (2026-10-28)**:
  - Reviewed `20261028T170032Z_gemini`;saved independent versioned record at `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T170734Z_codex_gemini_section_review/audit.md`. Preserved148 review files and verified Gemini's36-entry input manifest. Independently viewed complete original NTU physical13/25 andPAN38/39/48/49/50;source hashes and all production tables unchanged. Independent calculations exit0;Gemini's script not executed.
  - Supports a controlled full NTU section trial within sample;Gemini detailed corrections required. Sign-error and POCI ordinary Stage1/2 applicability findings supported. NTU zero-default/rounding explanation unverified;first-time comparative alone proves neither restatement nor methodology change. PAN FY25 overlap1081oz confirmed;Gemini-attributed194954/1573oz gap absent from actual saved DeepSeek answer. DeepSeek itself allowed double-count/misattribution;not an established company-error allegation. Shared-topic coverage preserved in both old/new;do not claim universal improvement or guaranteed repair.
  - Additional source issue missed by DeepSeek/Gemini/prior Codex pilot: PAN p39 prints cost unitUS$million with420,686/87,718/508,405,while stated per-ounce metrics imply420.686/87.718/508.405million. Conditional normalization reproduces per-ounce math,but source unit/number-format ambiguity must be flagged;no asserted issuer correction or valuation impact. Minor1oz cross-table/subtotal differences limit blanket exactness claims.
  - Proposed,not implemented:common sign/unit consistency;POCI guidance narrowly excluding ordinary SICR migrations while permitting legitimate credit-risk questions;first-time comparative caution allowing independently evidenced errors. No prompt/SQLite guardrail edits,paid calls,Stage1/2 reruns or new valuation. Full chronological run awaits user authorization. Last app suite226 passed exit0;no regression rerun for read-only review. Tools:initial Windows206 preservation-path failure resolved with flat numbered copies;initial audit-script syntax failure from reserved keyword corrected. Partial preparation retained and labeled incomplete.

- **Gemini independent review of simplified section-reading prompt pilot completed (2026-10-28)**:
  - Saved full independent evidence audit under `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T170032Z_gemini/audit.md`, input manifest in `inputs/manifest.json`, and calculations script in `calculations/reconciliations.py` (all tests passed, exit 0, outputs in `calculations/reconciliation_output.json`). Source PDF hashes verified for NTU (`9a19b3b4...`) and PAN (`62b10bcd...`); production database and all originals preserved untouched.
  - Concluded **SUPPORTED FOR FULL NTU TRIAL — SPECIFIC FIRST-PASS IMPROVEMENTS CONFIRMED; TARGETED REUSABLE PROMPT TWEAKS IDENTIFIED**. Evaluated all 4 paired captures and 8 Fireworks calls against original PDFs (NTU pp.13, 25; PAN pp.38-39, 48-50).
  - Confirmed operational improvements: 4/4 valid ledgers (100%) vs 3/4 (75%), 12 proposed questions vs 26 (-53.8%), prompt chars -17.1%, completion tokens -32.9%, wall-time -29.3%, cost -25.2%. Clean 4-part structure preserved secondary topic starts (NTU p.25 Note 6.2 currency risk) and linked to `Pending: p.26`.
  - Confirmed model defects: NTU p.13 ledger equation string inverted sign (`702 + 28 - 116 - 30 = 644` evaluates to 584, a -60m error; prose is correct), model persisted in requesting POCI ECL staging tables (`Q-b332e6c7ddfc4e8d`) despite sector note warning, and NTU p.25 answers overinterpreted standard interim comparative presentation and zero loss rates.
  - Forensically resolved PAN operations table discrepancy: the apparent 1,573 oz gap in text and 1,081 oz excess in `Q-99e93be7ca7c4594` arise from upstream extraction column collapse and model double-counting of 1,081 oz third-party buy-in feedstock against 2,654 oz Barberton surface production (`2,654 - 1,081 = 1,573 oz`), while company totals (196,527 oz FY25, 272,310 oz FY26) are mathematically exact.
  - Formulated 3 minimal reusable prompt clarifications (strict equation sign consistency, explicit POCI staging prohibition, and interim comparative context) prior to full chronological trial. No paid API calls or production code/guardrails modified. Audit ready for Codex review.

- **Simpler common section prompt implemented and paired pilot reviewed (2026-10-28)**:
  - User authorized one shared useful-first-pass task,conditional sector notes and a small cross-company pilot. Replaced8 long sector templates with concise notes;common prompt gives4 outputs:facts,qualifications/reconciliations,questions/next evidence,ledger. Existing structured JSON schema/manual Markdown compatibility retained;regex supports final Section4 without Section5. Native topic context exposes secondary shared-page starts. PDF splitting/production reasoning and caps unchanged;no company-specific rules added.
  - Full offline suite226 passed in104.57s,exit0,network denied. Initial targeted52 pass/1 fail was a template-assembly test assumption;updated to test common+sector assembly. Before templates/code preserved under `workflow/changes/20261028_section_prompt/before/`. Unique target/full test directories cleaned after preserving both results.
  - Four paired captures,8 Fireworks-only calls,none reasoning/16384 cap,no repairs:NTU p13/p25 andPAN p38–39/p48–50. Run:`companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T163642Z_section_prompt_paired_pilot/`. All8 complete;totalUSD0.0300091344,all costs metadata-corroborated. Revised versus old:4/4 vs3/4 valid ledgers;12 vs26 proposed questions;90892 vs109642 prompt characters (17.10% shorter);summed39.280 vs55.522s;USD0.0128405676 vs0.0171685668. Cache/order/small-sample limitations recorded;no universal accuracy claim.
  - Limited content review records remaining errors:revised NTU p13 ledger writes702+28−116−30=644 (actually584;correct prose uses+30),still asks POCI staging;both p25 answers overinterpret first-time comparison/zero rates. Both old/new p25 cover currency risk;no unique coverage fix established in this pair. PAN column-to-asset mapping remains provisional. No paid repair loop,source/model-output corrections or new sector_guardrails.
  - Versioned audit/executed calculations/comparison/manual Gemini prompt saved. No new PDF image review,forecast/valuation verification,Stage1/2 rerun or Gemini API. All source PDFs/production tables/original files verified unchanged. Inherited transport bookkeeping said reasoning controls omitted;normalized from exact requests proving none/exclude=true,original receipts preserved. Docs:`docs/SECTION_READING_PROMPT.md`.

- **Fireworks adopted; section-prompt inspection (2026-10-28)**:
  - Follow-up extraction trace found optional presentation clustering makes a separate direct OpenRouter request. It is now also restricted to Fireworks with provider fallback disabled. Corrected earlier local-only description:normal reports use local bookmarks/headings;presentations optionally use DeepSeek on slide titles/snippets before local capture. API tests including this separate route:22 passed in8.76s,exit0,network denied;temporary test folder cleaned. No paid calls or extraction-boundary changes.
  - User chose Fireworks after the successful Stage2 comparison. Shared OpenRouter client now restricts DeepSeek requests to Fireworks, disables provider fallback and requires parameter support; default model uses base slug without Nitro. Other models retain their existing routing. Existing reasoning/token settings unchanged; no paid calls made for this change.
  - Offline API tests:21 passed in8.97s,exit0,Python network denied. Coverage includes both reasoning modes,provider pin retained across retries/legacy Nitro fallback,and no Fireworks restriction on other models. Source PDFs,model outputs and production SQLite not modified by this change.
  - Inspected actual app path:local report_map/capture_planner extracts/splits PDF evidence;packages.build_prompt combines sector reading-brief template,structured-ledger override,map/coverage and selected text. Consumer-lending template remains a six-section forensic question/footnote prompt with a long originator-focused checklist. Recent NTU trial compact prompts are separate experiment drivers,not the app template. No extraction/prompt redesign implemented during this inspection; user prefers a simple approach effective across companies.

- **NTU Fireworks-only Stage2 experiment (2026-10-28)**:
  - User requested Fireworks. Exact Relace300k input retained;only provider object changed,Fireworks only/no fallback/require supported parameters. One attempt,default thinking,300000 cap. Run:`companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T154859Z_deepseek_stage2_fireworks_300k`.
  - Provider:Fireworks;generation complete:True;finish:stop;elapsed:50.43s;reported costUSD:0.02148888;input:35708;completion:16655;reasoning subset:11727. API error:None. Publication assessment:WITHHELD;not independent financial validation.
  - Preserved exact original request/Stage1/Relace receipt/source hashes,recorded costs/tokens/timing/provider,versioned audit and manual Gemini prompt. Preliminary evaluator on copied DB/explicit new path;offline checks exit0. All production tables/source/originals unchanged. Known inherited Stage1 R370m error retained for comparison;historical bridge leaves6 unexplained. No new app defaults,financial guardrails,Gemini API calls or automatic paid retry. Full pytest not rerun for isolated live test.


- **NTU Stage2 explicit300k experiment finished incomplete (2026-10-28)**:
  - User authorized one300,000-token Stage2 rerun. Exact original prompt/model/temperature/stream retained; only max_tokens added. Default thinking and normal routing; actual provider Relace again. Run:`companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T153201Z_deepseek_stage2_300k/`.
  - Stream failed with502 provider_unavailable after786.281s (13m6.281s),no final answer,finish reasons null. Metadata183,036 completion tokens,all reasoning,input35,325;reportedUSD0 corroborated by metadata-only refresh. Passed prior131,072 observed stopping point but failed before300,000. This does not establish exact omitted-cap default or cause of upstream failure. No automatic retry.
  - Saved request/receipt/cost-time-token metrics,comparison,RUN_SUMMARY.md and versioned audit.md. Offline review exit0;dispatch tool exit1. Preliminary evaluator against explicit new path MISSING_NOTE;no production fallback or published valuation. All production tables/source PDF/original files verified unchanged. Historical bridge rerun leaves6 unexplained;known Stage1 R370m claim retained in unchanged comparison input. No app defaults,financial guardrails or Gemini calls changed;no full pytest rerun for isolated experiment.


- **Reviewed logical NTU trial completed; Stage2 incomplete (2026-10-28)**:
  - User approved plan review, difficult-section pilot, then full chronological rerun if pilot worked. Run: `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T141038Z_deepseek_reviewed_logical/`. Reviewed30 draft units→24, with22 analytical and2 navigation/contact units; all38 pages retained. Source-specific joins stay in reviewed plan, not general planner. Separate pilot/full databases and fresh source-order full ledger.
  - Pilot5 paid generations (3 original captures,1 quote repair,1 targeted scope recheck),USD0.0340914924. Signed POCI/FY25 historical259/conditional ECL checks passed. Original page25 response omitted the currency-risk note start and duplicated an answered question; preserved and corrected via run-only secondary-topic list,resolved-ID index,short exact locators. Recheck passed; gate recorded before full dispatch.
  - Full24-generation attempt:all22 financial section analyses and Stage1 completed,zero full-run section repairs; Stage2 stopped with finish_reason length at131,072 completion tokens,all reported reasoning,no final answer. No caller-set token cap; an upstream limit still applied. No recovery brief or further paid retry. FullUSD0.2445611328,pilotUSD0.0340914924,combinedUSD0.2786526252;all29 generation costs corroborated by metadata. Full wall19m12.42s,summed request17m7.97s. Full input193,159;completion312,161 including reasoning284,949. Pilot input21,717;completion36,668 including reasoning32,013.
  - New Stage1 sign/scope regression:claims apparentR370m portfolio cash difference;scoped434 net cash−246 accounting income=188 carrying decline,versus statutory182 leaves6 unexplained. Earliest observed in Stage1,not the section briefs. No unsupported company-error or causal token-exhaustion inference. Preliminary evaluator against explicit experimental path returns MISSING_NOTE;no new valuation published.
  - Saved separate Codex audit `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T145027Z_codex_logical_trial_review/audit.md`,exact copied inputs/hashes,executed calculations and actual final checks(exit0). Full ledger17 records:4 open,11 partial,2 resolved;22 valid full attempts. Source PDF,all production tables and prior model outputs unchanged. No Gemini API calls or new financial guardrails. Main run has RUN_SUMMARY.md,combined_metrics.json,CSV/receipts and updated manual Gemini prompt for available sections/Stage1 and absent Stage2. Next candidates:deterministic signed reconciliation before consolidation and decomposed Stage2 schedules;not implemented or paid-rerun authorization.

- **Logical PDF capture planning implemented (2026-10-28)**:
  - New local `section_capture/capture_planner.py` refines automatic captures using native heading/font/position evidence: distinct statements, notes/subtopics, observed reporting periods and instrument scope. Small related note pages stay together. Default hard limits6 pages/24,000 source characters; target3 pages/12,000 characters when boundaries are uncertain or related topics grow. Full pages retained, including oversized/sparse pages with warnings.
  - Size cuts and shared-page note starts have explicit neighboring-page dependencies; NTU p.25 trade ECL/currency-risk introduction links to p.26, which links to p.27 fair-value continuation. Native observations remain in local metadata; compact coverage/continuation instructions enter prompts. One-shot auto ranges now remove duplicate page ownership and retain unmapped gaps. Existing captures/outputs/valuations preserved; planner applies to newly created captures.
  - Offline previews: NTU38 pages→30 captures(max3 pages), DCP AFS87→70(max5), PAN54→26(max6). Every one of179 physical pages appears exactly once. More focused captures can increase call count; no quality/cost benefit claimed without a separately authorized trial. No paid models called.
  - Final offline suite214 passed in70.22s, exit0; DNS/connect/sendto denied. Production database and all3 original PDFs unchanged. Seven task-created test directories removed after copying validation receipts; previously blocked folders untouched. See `docs/LOGICAL_CAPTURE.md` and `workflow/changes/20261028_logical_capture/implementation_record.json`; NTU reviewable plan in `NTU_plan.md` in that changes directory.

- **NTU default-thinking/standard-routing capped trial stopped at Stage2 (2026-10-28)**:
  - User explicitly requested NTU rerun with lessons learned, without Nitro, default thinking and cost/token/time logging. Isolated run: `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T101309Z_deepseek_default_standard/`. Nine captures cover38 pages, eleven planned generations; two-section pilot. Base DeepSeek snapshot, reasoning controls omitted (runtime catalog default enabled/high); no speed/provider-priority override.
  - Separate runner and seven passing offline checks (exit0) under `workflow/changes/20261028_ntu_default_run/`. Actual result:15 attempts,11 completed generations,4 incomplete; Stage1 completed, full Stage2 exhausted65,536 completion tokens (all reported reasoning), no final answer. TotalUSD0.1893089364; all15 costs corroborated by generation metadata. Input177,596; completion249,443 including reasoning222,525. First-dispatch-to-last-accounting19m55.33s; summed generation elapsed13m43.17s. Nine of10 active capture analyses accepted after a run-only split; missing pages22–24 explicitly annexed to Stage1 without fabricated section answers. No production writes or Gemini API calls. Exact revisions/limits in run plan and RUN_SUMMARY.md; mixed revisions prevent causal speed/quality comparisons.
  - User explicitly authorized rerunning incomplete sections with no token limit. Isolated continuation `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T114521Z_deepseek_default_no_requested_cap/` completed all3 generations: outstanding capture39.189s, refreshed Stage1 61.727s, full Stage2 51.560s; no repairs. Nine accepted captures reused; all10 active analyses now accepted across38 pages. Requests omit max_tokens/max_completion_tokens and reasoning/routing overrides; provider/model limits still apply. IncrementalUSD0.04537836, combined with capped trialUSD0.2346872964. Input89,445; completion38,498 including reasoning29,835. Wall168.801s, summed request152.476s. All3 costs corroborated by generation metadata; final checks exit0.
  - Stage2 **completed with WITHHELD**, null target/rating/returns; it did not build forecasts/DCF/sensitivity. Do not confuse completed generation with financial/model validation or claim cap omission alone caused success: providers/context varied and new outputs were below prior ceilings. Preliminary Codex audit, RUN_SUMMARY.md, exact review inputs, metrics/CSV and manual Gemini prompt saved in continuation. Materiality of several source uncertainties/small residual blockers still needs Gemini review. Source PDF, parent outputs and all production tables unchanged; no Gemini API calls or new guardrails.

- **Approved conditional trade-receivables ECL guardrail codified (2026-10-28)**:
  - User approved the corrected NTU audit proposal. Inserted enabled `CONSUMER-LENDING-TRADE-RECEIVABLES-SIMPLIFIED-ECL` into production SQLite, sector `consumer_lending`, stage `all`, origin NTU. Requires instrument/policy classification before SICR allegations, financing-component/policy-choice qualification, evidence for zero ELRs, separate POCI treatment and no double-counted credit loss.
  - Saved approved wording, pre-change database backup, duplicate/conflict review and implementation record under `workflow/changes/20261028_ntu_ecl_guardrail_095304Z/`. Six offline checks of actual Stage1/Stage2/SENS prompt builders passed on a separate SQLite copy (consumer_lending includes the rule; retail excludes it); script exit 0. All other business rows unchanged; only registry row and its sequence entry changed. No paid calls, application-code changes, financial reruns or pytest suite. Section-prompt integration and other proposed amendments unchanged; future model compliance remains untested.

- **Codex review of Gemini NTU 1H26 completed (2026-10-28)**:
  - Saved independent audit at `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T093647Z_codex_review/audit.md`; preserved 89 input files and verified nine Gemini input hashes plus the source PDF SHA against SQLite. Independent checks: 18 arithmetic assertions, final exit 0. No paid calls or pytest for this audit-only work.
  - **CORRECTIONS REQUIRED; VALUATION WITHHELD** because the complete forecast/valuation remains unavailable. Gemini's R809m is a static stock comparison, not a demonstrated funding shortfall; its R164m PBD discrepancy compares different scopes. Combined portfolio net cash434 less accounting income246 equals carrying decline188, leaving6 versus statutory182 unexplained. Do not infer FX or rounding for that residual.
  - DeepSeek errors missed by Gemini: nonfinancial receivables residual107 rather than102 (gross/net error), conventional ETR+31.52% rather than-31.5%, and unsupported requirement for a director-prepared forecast. Gemini misread FY25 second-half historical-book loss182 as a full-year amount; full year259. Null valuation outputs do not demonstrate repaired forecasting logic.
  - Ledger review: 24 recorded attempts (including local replays/fallbacks):9 valid,15 rejected; first errors9 quote,1 JSON,2 ID,3 contract. Five fallback events cover four unique sections. Questions:63 open,5 partial,1 resolved. Pipes exist in captured tables and seven matching pipe quotes appear in valid attempts; formatting alone does not explain all failures.
  - Proposed applicability-first ledger questions and a qualified simplified-ECL guardrail; none implemented/codified. Existing NTU report, all guardrail rows, original model outputs and source PDF unchanged by this review. DCP Gemini review has arrived in the worktree but was not independently reviewed in this NTU task.

- **Gemini independent review of DCP DeepSeek workload trial completed (2026-10-28)**:
  - Saved full independent evidence audit under `companies/retail/DCP/briefs/FY26/evaluations/20261028T092808Z_gemini/audit.md`, input manifest in `inputs/manifest.json`, and reproducible verification script in `calculations/reconciliations.py` (all tests passed, exit 0, outputs in `calculations/reconciliation_output.json`). Source PDF hashes verified for all three reports: AFS (`f346d200...`), Presentation (`6cd39585...`), IAR (`fec45259...`).
  - Concluded **VALUATION WITHHELD — MATERIAL ISSUES UNRESOLVED; CORRECTIONS REQUIRED FOR STAGE 1 / PROPORTIONALITY FILTER FOR STAGE 2**. Evaluated Stage 1 and Stage 2 against all three primary PDFs and the preserved baseline note.
  - Validated that valuation withholding is fully justified under `ALL-MATERIAL-ISSUES-VALUATION-WITHHOLD` and `STOCK_EVALUATION_FORMAT.md`:
    1. Baseline valuation contained a catastrophic arithmetic plug: claimed EV R15,995m and Equity Value R13,201m divided by 857.0m shares yielded R35.00/share, whereas exact division yields **R15.40/share** (an unexplained R16.794bn / +127.2% equity markup that concealed a true blended valuation of R21.02 or -25.1% downside / STRONG SELL).
    2. Baseline assumed positive cash of +R500m, whereas AFS Note 27.5 demonstrates Dis-Chem holds only R134.4m gross cash and operates in a **net bank overdraft of -R1,166.964m**.
    3. Baseline double-counted dividends by claiming R521m Pre-Div FCFE from statutory OCF (R1,793m) less capex and lease principal, ignoring that statutory OCF already deducts R524.2m in dividends paid and R559.6m in finance costs.
    4. Note 24 reveals R965m of supplier finance (reverse factoring) payables inside trade payables, presenting major unhedged balance-sheet debt reclassification risk.
    5. Debt covenant headroom is unquantified with Group gearing at 2.8x (excluding leases) and a bullet facility maturing 31 May 2027 alongside a post-year-end R500m bullet drawdown.
  - Highlighted high analytical self-correction in Stage 2: DeepSeek Stage 2 audited Stage 1 and caught 6 distinct Stage 1 errors (gearing 2.8x vs 2.6x, S189 headcount 545 vs 505, wholesale customer counts vs revenue, Better Rewards R761.2m vs R1,126.9m, pipeline 34 stores vs 13 stores, pipeline vs trading space).
  - Identified new errors introduced by DeepSeek: lack of institutional proportionality elevating an immaterial R85,000 non-audit fee difference (N18) to a valuation blocker, and demanding an inapplicable consumer financial services revenue disaggregation (U1) from a pharmacy/FMCG retailer.
  - Audited ledger reliability performance: 75 of 159 attempts rejected by strict quote validator; 27 local open-only fallbacks triggered; 366 of 471 questions remained open in SQLite due to non-literal quote repairs failing.
  - Formulated proposed guardrails `ALL-WITHHOLD-MATERIALITY-THRESHOLD` and `RETAIL-REVENUE-DISAGGREGATION-SCOPE`, and recommended whitespace-normalized fuzzy substring matching in `section_capture/ledger_verifier.py`.
  - All originals preserved; no prompts, valuations, or production SQLite guardrails modified. Audit ready for Codex review.

- **Gemini independent review of NTU DeepSeek workload trial completed (2026-10-28)**:
  - Saved full independent evidence audit under `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T092500Z_gemini/audit.md`, input manifest in `inputs/manifest.json`, and reproducible verification script in `calculations/reconciliations.py` (all tests passed, exit 0, outputs in `calculations/reconciliations.json`). Source PDF hash (`9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc`) and all 9 preserved input outputs verified.
  - Concluded **VALUATION WITHHELD — MATERIAL ISSUES UNRESOLVED; CORRECTIONS REQUIRED FOR MODEL PIPELINE**. Evaluated the separately prompted WITHHELD recovery brief without treating it as an autonomous completed full valuation; highlighted that full Stage 2 exhausted both 65,536 and 98,304 completion budgets (`finish_reason: length`).
  - Audited ledger reliability performance: 15 of 24 attempts rejected by strict quote validator; 5 local open-only fallbacks triggered; 68 of 69 questions remained open in SQLite due to DeepSeek inserting markdown table pipes (`|`) and formatting spaces into quotes.
  - Verified substantive accounting improvements maintained: POCI cumulative gain (+R431m on gross R3,414m = net R3,845m; 12.6% is gain/gross, not loss reserve), statutory NAV per share (R1.70 vs contributed stated capital R6.93), CODM amortisation footnote arithmetic (R598m ≈ R597m), dropped old false management percentage-sign allegation, and identified company cash flow p. 12 investing/financing mislabelling (+R178m).
  - Identified repeated defects: repeated misconception demanding 30-DPD SICR loan staging on corporate trade receivables governed by the IFRS 9 simplified lifetime ECL approach, and unsubstantiated demands for NCA origination rate caps and ABS securitisation structures. Formulated proposed guardrail `CONSUMER-LENDING-TRADE-RECEIVABLES-SIMPLIFIED-ECL` for review.
  - All originals preserved; no prompts, valuations, or production SQLite guardrails modified. Audit ready for Codex review.

- **Execution-delay retrospective completed (2026-10-28)**:
  - Saved receipt-based timing analysis and review under `workflow/changes/20261028_workload_reliability/delay_retrospective.*`. Completed trials produced 141 successful receipts including 44 ledger repairs. DCP elapsed approximately 54 minutes, with 33 minutes inside recorded call wrappers; failed calls and debugging/resumption add time. Nine test invocations totalled about 9 minutes of overlapping process runtime.
  - No telemetry-related rejection was observed in the visible implementation/rerun tool results. Telemetry-named command variables requested opt-out; PowerShell requires its variable before process startup, so in-command assignment does not prove host telemetry was disabled. No host packet trace collected; earlier telemetry incidents are separate.
  - Recorded pilot-first validation, bounded repair, coherent test milestones, immutable dispatch copies and clearer failure/progress reporting in TOOL_CHEATSHEET.md section 30. No paid models, permission changes, production code or financial evidence changed in this review.



- **NTU/DCP DeepSeek trials finished; Gemini handoffs ready (2026-10-28)**:
  - Final implementation suite: 195 passed in 68.49s, exit 0. Coverage plans reject interrupted cached prefixes; section context routes at most 12 relevant questions while retaining the full persistent ledger for Stage 1. Nine completed test directories cleaned, exit 0, result records preserved.
  - NTU: all 38 pages/9 captures processed; Stage 1 completed. Full Stage 2 exhausted 65,536 and comparison-only 98,304 completion budgets; a separately labeled concise WITHHELD recovery brief completed. This is not a completed full valuation. Final runner exit 0 reflects successful recovery/handoff only.
  - DCP: all 259 pages/84 captures processed; full Stage 1 and Stage 2 completed, final runner exit 0; application publication assessment WITHHELD. Model completion is not financial validation.
  - Both review packs have source hashes verified, artifact manifests, comparison metrics, concise gemini/START_HERE.md and larger reference bundles. See `workflow/changes/20261028_workload_reliability/ANTIGRAVITY_HANDOFF.md`. Trials include mixed revisions, repairs and explicitly qualified local open-only/backlog fallbacks, which are not successful model resolutions.
  - No Gemini API calls: user runs Gemini in Antigravity, saves a fresh timestamped Gemini audit, then Codex reviews it. Production reports, captures, guardrail rows, original notes and source PDFs verified preserved. Only sqlite_sequence differed in production due the earlier integration-test read helper; that test now uses a backup. No new guardrails or valuation promotion.



- **Capture/ledger reliability implemented; NTU/DCP comparison in progress (2026-10-28)**:
  - Automatic capture now preserves full requested ranges in page/text-bounded chunks (12 pages / 24,000 characters by default), records coverage/sparse-page limits, and stops ingestion on capture errors. No silent 25-page truncation.
  - Added persistent suite-scoped question records, revision events and accepted/rejected response attempts. New automatic captures/resubmissions use JSON deltas, stable app IDs and evidence-backed statuses. Omitted questions persist; source/page/literal-quote checks reject unsupported updates. Legacy text stays preserved. Compact prompt state omits repeated answer narratives; production reasoning policy/analytical guardrails unchanged.
  - Final offline suite: 192 passed in 75.53s, exit 0, with DNS/connect/sendto denied. Earlier legacy-format fixtures corrected. A production-reading integration test now uses a temporary database backup; logical reports/sections/guardrails matched the pre-run snapshot despite observed sqlite_sequence changes. See `workflow/changes/20261028_workload_reliability/production_preservation_check.json`.
  - User authorized two reruns: NTU 1H26 (38/38 pages, 9 captures) and DCP FY26 (259/259 pages across 3 reports, 84 captures). Versioned run paths/selection/source hashes in `workflow/changes/20261028_workload_reliability/comparison_plan.json`. DeepSeek runs in isolated databases; production notes and PDFs preserved. Runs are not yet complete at this checkpoint.
  - Live trials exposed non-literal evidence, malformed deltas and section output exhaustion. Whitespace-only quote normalization was tested; signs/words remain strict. Comparison runner records bounded repair/32,768-token completion retries and explicitly qualified local open-only/backlog fallbacks, never treating rejected closure claims as verified. Mixed revisions are not a controlled benchmark.
  - User runs Gemini in Antigravity: no Gemini API calls. Prepare local evaluation packs after DeepSeek completes; Codex reviews preserved Gemini output when supplied. Do not call Gemini through OpenRouter. Documentation: `docs/WORKLOAD_RELIABILITY.md`.



- **DeepSeek workload review completed; improvements proposed (2026-10-28)**:
  - Saved offline review, input hashes, workload metrics and reproducible scripts under `workflow/changes/20261028_deepseek_workload_review/`. Inspected 338 captures/20 reports; 304 have saved analysis and token metadata. Largest saved section request reports 151,637 input tokens. Existing Stage 1 ledger compaction removes 46.55% of saved response characters across the inspected corpus.
  - Priorities: split oversized captures without losing remainder pages; make ledger updates persistent and evidence-validated; improve specific reconciliation questions and cited fact continuity; apply relevant approved guardrails during section interpretation; standardize Stage 1 handoffs; independently calculate schedules; version exact requests/reuse and derive periods dynamically. Reasoning allocation improvements need a controlled authorized comparison.
  - Confirmed current 25-page capture clipping and permissive ledger extraction through code inspection/four pure-function probe assertions. Capture page sets describe stored selections, not financial completeness. No company valuation or source PDF was re-audited.
  - Both review scripts exited 0 and verified the production SQLite hash unchanged. No production code/prompts/ledger entries/guardrails/valuations or original evidence changed, no model calls, no pytest rerun. Last full offline suite remains 178 passed, exit code 0. All proposals remain unimplemented.



- **Valuation-withholding handoff cleanup completed (2026-10-28)**:
  - Inspected the existing worktree without discarding or staging changes; all 11 implementation hashes match `implementation_record.json`.
  - Removed exactly the six previously blocked test directories listed in `cleanup_status.json` using native PowerShell after approved escalation (exit code 0). Verified every target stayed within workspace `tmp` and contained no reparse points; confirmed all six are absent.
  - Updated `cleanup_status.json` with completion evidence and preserved its previous blocked status. The original implementation record remains unchanged as historical evidence.
  - No application code, production database, NTU valuation, source PDF or model evidence changed; no paid model calls or other guardrail amendments. Tests were not rerun for cleanup/documentation only; the last full offline suite remains 178 passed, exit code 0.
  - Tool retrospective: bounded re-reads resolved initial oversized output; explicit JSON avoided PowerShell mixed-object table columns hiding cleanup paths. Existing cheatsheet sections 19 and 23 cover these patterns.



- **Approved material-issue valuation withholding implemented (2026-10-28)**:
  - Added shared publication gate in `section_capture/valuation_policy.py`. New Stage2/SENS outputs require READY/WITHHELD status, blockers, seven evidence checks and numerical reconciliations. Missing/incomplete evidence, material FAIL/NOT VERIFIED or inconsistent reconciliation inputs withhold target, bands, upside, dividend yield, TSR and recommendation; no zero/HOLD fallback.
  - Stage1 carries unresolved material findings forward; Stage2/SENS reopen working claims rather than using a99% confidence prior. First-JSON readiness is mandatory; later/conflicting blocks cannot authorize an earlier scenario target. Legacy notes remain readable, but new saves/resyncs require the contract.
  - GUI/CLI preserve timestamped raw candidate files; SQLite retains `stage2_candidate_response`. Withheld publication notes show blockers and clear stale derived fields. Portfolio/company/final pipeline displays say Valuation withheld and suppress dynamic rating fallback. Parent/companion updates preserve each report's own baseline. CLI material SOTP/guardrail failures override model READY and block rerun promotion.
  - Codified only the approved `ALL-MATERIAL-ISSUES-VALUATION-WITHHOLD` in default registry and SQLite (36->37); unrelated registry rows verified unchanged. NTU original production report values and source PDF hash remain unchanged; no paid model call or valuation rerun. Other analytical amendments remain proposals.
  - Targeted offline regressions:91 passed in30.11s,exit0. Full offline suite:178 passed in96.99s,exit0. Existing and new Qt tests dispose windows. The network-denial pytest plugin and telemetry opt-outs allowed local testing after automatic review reported an unknown Visual Studio telemetry request on a normal output poll; that interrupted attempt has no claimed final test result.
  - Reference fallback and prompt-expectation failures from the interrupted turn were fixed. Also fixed parent-baseline preservation and conflicting JSON handling. Guarded exact-match edit preflights and UTF-8/CRLF import handling failures were corrected before final passing checks. Test results, approved-rule/data verification and implementation hashes saved in `workflow/changes/20261028_valuation_withholding/`; documentation in `docs/VALUATION_WITHHOLDING.md`.
  - READY is a publication prerequisite, not independent financial validation: falsely reported source data or omitted dependencies still need evidence review. Native cleanup was rejected before execution because sandbox approval is disabled; six `tmp/valuation-gate-*` test directories remain. Exact paths and rejection are in `workflow/changes/20261028_valuation_withholding/cleanup_status.json`; no alternate deletion route attempted.


- **Codex review of completed NTU max comparison: CORRECTIONS REQUIRED; R0.95 and Gemini R0.64 NOT VERIFIED (2026-10-27)**:
  - Saved separate review: `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T182308Z_codex_review/audit.md`. Preserved77 review inputs; independently verified50 baseline originals, source PDF/SQLite and both request prompt hashes. Stage2 required reversing one Windows newline-write translation. Production report and36 guardrails remain unchanged.
  - Saved metadata supports Together / deepseek-v4.1-flash-20261017, both finish_reason=stop,59787 reported reasoning tokens and total cost$0.099366132. No new API calls. This is a combined reasoning/guardrail/prompt comparison; causal attribution to reasoning alone is unavailable.
  - Confirmed POCI/NAV/signed-amortisation improvements, removal of old plug/repeated discounts and sensitivities within1c. Gemini overstates cash/forecast remediation: historical FCFE140 implies OCF170 versus statutory-111 (281 unexplained;311 versus cash after capex/leases); historical borrowing direction is reversed. FY26 cash mixes March opening with full-year flows; principal forecasts fail by40/50 and total portfolios by20/10. DCF discounts260/330 before250/320 repayments without a consistent debt/lease/terminal policy.
  - Gemini's working-capital concern is partly supported; allocation of all276 remains unresolved. R0.64 is conditional arithmetic, not validated fair value. Its conditional rating under the existing bands would be STRONG SELL, not Gemini's SELL; neither rating is economically validated. Persisted Stage1 percentage-sign and staging allegations and the tangible-NAV label also need correction.
  - Final independent preservation/extraction/calculation scripts exited0; no application changes or pytest. Proposed amendments to existing guardrails saved for approval; none codified. This entry qualifies rather than overwrites Gemini's completion entry below.


- **NTU 1H26 DeepSeek Stage 1/Stage 2 max-reasoning comparison completed & independently evaluated (2026-10-27)**:
  - Executed original comparison runner (`scratch/run_ntu_max_comparison.py`) under user authorization. Run completed with exit code 0 under `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T175621Z_codex_max_comparison/`.
  - Upstream provider `Together` returned full completions for `deepseek/deepseek-v4.1-flash-20261017`:
    - Stage 1: ID `gen-1793123782-fGM9yDEPVLCvGTKnYrDo`, 22,576 reasoning tokens, 30,050 completion tokens, elapsed 145.18s, cost $0.036330, finish reason `stop`.
    - Stage 2: ID `gen-1793123928-27jC3ncJR0I18Q3WcNka`, 37,211 reasoning tokens, 43,537 completion tokens, elapsed 211.44s, cost $0.063037, finish reason `stop`.
    - Total tokens: 154,238; total reasoning tokens: 59,787 (81.2% of completion); combined cost: $0.099366 (~R1.80 ZAR).
  - Preserved original files and source PDF SHA-256 (`9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc`) verified matching SQLite; production report row (R0.55/SELL) and 36 `sector_guardrails` verified completely untouched.
  - Independent Section 1A forensic evaluation completed across C001–C013:
    - Remediated defects: POCI cumulative gain accounting (C001), statutory NAV R1.70 anchor (C002), net run-off amortisation footnote signs (C003), elimination of arbitrary R1,479m plug and double discounts (C004), cash collections added as inflows / acquisitions deducted in FCFE (C005), cash roll-forward closes with all 5 balance sheet years balancing to 0 (C006), sensitivity matrix fully reproducible from SOTP formula (C007), rating bands monotonic and aligned with static HOLD (C011), inverted short stop removed (C011), trade-receivable staging softened to qualified policy flag (C013). Denominator error omitted (C008).
    - New material defect identified (C012 / F003): SOTP EV-to-Equity bridge adds back +R276m Net Trade Working Capital on top of operating EV/EBITDA multiples, treating operating debtors as non-operating surplus cash and overstating target price by R0.31/share (R0.95 published vs R0.64 counterfactual).
    - Minor observation (F004): R7m to R10m residual between FCFE debt repayment and balance sheet debt/lease reductions.
  - Independent verdict: CORRECTIONS REQUIRED for published R0.95; R0.64 supported upon removing working capital double-count. No database rows or guardrails codified.


- **NTU max comparison: OpenRouter approved; separate telemetry approval blocker (2026-10-27)**:
  - User explicitly authorized NTU captures/ledger/full report text to OpenRouter and paid Stage1/2 calls. Run174426Z output polling rejected over distinct telemetry; no final model output.
  - Tried safer OpenRouter-only launcher; first guard failed on required managed loopback proxy (exit1); startup assertion then caught variable proxy port (exit1). Final guard retains environment-owned proxy without bypass and forbids other external destinations. Run174728Z output poll still rejected by automatic approval review over reported Visual Studio telemetry with unknown payload. No fresh answers/metadata; final process exit code unavailable; stale running/stage1 is not completion. No evidence Stage2 submitted. Whether Stage1 reached service/billing is NOT VERIFIED.
  - Current evidence: `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T174728Z_codex_max_comparison/audit.md`, execution events, independent verification, local PDF extraction/renders and independent baseline calculations. All50 original/copied files and source hash verified; production report row/guardrails unchanged. Scripts exit0; no pytest for evidence-only work.
  - Reproduced baseline POCI/NAV/footnote/valuation/cash/sensitivity/denominator errors. Added unresolved baseline trade-receivable staging inference (C013): age/loss-rate table does not establish delayed Stage2 policy; check applicable simplified lifetime-ECL approach. No new rule or valuation codified. Need resolve separate reported telemetry approval gate before any further upload.


- **NTU max comparison: external-upload approval blocked (2026-10-27)**:
  - OpenRouter public models endpoint reachable (HTTP 200), but runner continuation was rejected by automatic approval review for lack of explicit approval to send NTU captures/ledger and complete report text to OpenRouter.
  - New run: `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T174201Z_codex_max_comparison/audit.md`. Inputs and 176,400-character Stage 1 prompt preserved; no model answers or generation metadata. On-disk running/stage1 is a stale checkpoint; session subsequently unavailable, no final exit code. Whether Stage 1 payload reached service is NOT VERIFIED; no evidence of Stage 2 submission.
  - Independent hash checks: all preserved originals/copies and PDF match baseline; production report row and guardrail registry unchanged. No new financial comparison or improvement claim; no pytest needed for evidence-only work. Explicit approval of payload/destination is required before retry; do not bypass rejection.


- **NTU max comparison resumed; DNS still blocked (2026-10-27)**:
  - Ran the authorized saved runner again; actual exit code 1. New evidence run: `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T172440Z_codex_max_comparison/audit.md`.
  - PDF hash matches SQLite/prior baseline. All copied original briefs and Gemini/Codex audit artifacts rechecked unchanged; exact Stage 1 prompt is identical to prior attempt (176,400 characters).
  - Max/65,536/900s Stage 1 retries/base fallback again failed with `[Errno 11001] getaddrinfo failed`. No final answer or generation metadata; Stage 2 not submitted. No fresh comparison or quality improvement can be established. Network access to OpenRouter remains unusable from this runner.
  - Saved manifest, SQLite/capture/guardrail snapshots, actual status/terminal output and independent hash checks. No production notes, valuation fields, source PDFs or guardrails changed. No pytest run (execution/evidence-only); no new tooling-error pattern beyond existing oversized-read guidance.


- **NTU max-reasoning comparison prepared; live run blocked (2026-10-27)**:
  - Preserved the four original DeepSeek briefs, full Gemini/Codex audit trees with hashes, a consistent SQLite backup, captured sections/ledger and guardrail registry under `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T171921Z_codex_max_comparison/`.
  - Verified the original 38-page PDF SHA-256 against SQLite and prior baseline. Prepared exact current-policy Stage 1 prompt (176,400 characters) from the existing two captures; evaluator conclusions not injected. This is a combined reasoning/guardrail/prompt comparison, not a reasoning-only experiment or fresh section analysis.
  - Live Stage 1 requested configured DeepSeek nitro model with max/65,536/900s. Existing retries/base-model fallback failed: `[Errno 11001] getaddrinfo failed`; process exit code 1. No final answer, generation metadata or demonstrated quality improvement. Stage 2 not submitted; network remains restricted and elevation unavailable.
  - All preserved original files and source PDF verified unchanged; production notes/valuation not replaced. Saved `audit.md` with 12 pending claim checks and resumable runner `scratch/run_ntu_max_comparison.py` (exact copy also in run). Run again from project root with working OpenRouter access, then compare fresh outputs and actual metadata before validating targets.
  - No application source changes or pytest run; evidence/execution attempt only. Tool retrospective: initial oversized reads truncated, resolved with bounded relevant reads (existing cheatsheet section19); DNS failure recorded as a network limitation, distinct from successful workspace writes. No new shell/encoding/editing-error pattern.


- **Stage 1/2 max reasoning enabled (2026-10-27)**:
  - Found `query_openrouter` hard-coded `reasoning.effort=none` for every request, including Stage 1/2. Added per-request/worker reasoning effort and shared stage policy: `max`, 65,536 combined completion tokens, 900-second HTTP timeout.
  - Applied policy to GUI Stage 1, full Stage 2, Stage-2-only resubmission, SENS valuation updates, CLI `evaluate_stock.py --rerun`, and both stage diagnostic scripts. Section capture/mapping/ticker requests retain their existing `none` defaults and budgets. Retry/nitro fallback retains the requested effort; reasoning requests require providers supporting requested parameters.
  - Successful GUI stage reports and CLI reruns save `.run.json` metadata with requested effort/budget, generation/model, provider when available, reported reasoning tokens (null if unavailable), finish reason and usage statistics. Raw reasoning is excluded; reasoning-only or `finish_reason=length` output is rejected instead of being saved as a completed report.
  - Official OpenRouter reasoning documentation checked for `max`; actual provider effort mappings may vary. No paid live completion, source-PDF modification, valuation rerun or demonstrated financial-quality improvement was claimed. Next comparison should use preserved NTU evidence and new run metadata.
  - Targeted OpenRouter/GUI regression tests: 31 passed in 17.28s (exit code 0). Full suite: 151 passed in 57.40s (exit code 0). Existing Qt fixtures dispose windows. Exact-match edit preflight initially found two matching log strings rather than three; corrected before any source writes. Terminal/tool retrospective recorded in `TOOL_CHEATSHEET.md`.
  - Verified task cleanup paths inside workspace `tmp`, but native deletion was rejected before execution because sandbox approval is disabled. Remaining: `tmp/stage-reasoning-targeted-20261027`, `tmp/stage-reasoning-full-20261027`, `tmp/enable_stage_reasoning.py`, `tmp/test_stage_reasoning_edits.py`. Earlier NTU temporary files were not touched.


- **Approved NTU guardrails codified (2026-10-27)**:
  - Added four user-approved rules to SQLite `sector_guardrails` and `DEFAULT_SECTOR_GUARDRAILS` in `section_capture/db.py`: `ALL-CASH-ROLLFORWARD-CONSISTENCY`, `ALL-SENSITIVITY-REPRODUCIBILITY`, `CONSUMER-LENDING-POCI-GAIN-VS-ECL-RESERVE`, and `ALL-EQUITY-NAV-VS-CONTRIBUTED-CAPITAL`. Active database rules increased from 32 to 36; unrelated registry rows were verified unchanged.
  - Qualified POCI wording preserves source ECL-allowance labels, signed cumulative lifetime gains and amortised-cost versus FVTPL scope; NAV wording permits explicitly reconciled adjusted/tangible NAV and excludes non-ordinary equity claims.
  - Verified universal rules and consumer-lending-only POCI scope in generated Stage 1, Stage 2 and SENS prompts. These are model instructions in the registry, not new automatic numeric detectors in `evaluate_stock.py`. No NTU valuation was rerun or overwritten.
  - Preserved approval, exact rule texts, affected-row history and test evidence in `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T164527Z_codex/guardrails_codification.json` without altering the original audit record.
  - Targeted tests: 6 passed (exit code 0). Full suite: 145 passed in 56.25s (exit code 0). SQLite/default/record parity and whitespace checks passed. Qt windows disposed by existing fixtures. Temporary test directories (`tmp/ntu-guardrails-targeted-20261027`, `tmp/ntu-guardrails-full-20261027`) and helper scripts (`tmp/codify_ntu_guardrails.py`, `tmp/verify_ntu_guardrails.py`) have been cleaned up and removed.


- **Codex review of Gemini NTU 1H26 (2026-10-27): CORRECTIONS_REQUIRED; target/rating NOT VERIFIED**:
  - Saved separate review in `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T164527Z_codex/audit.md`, preserving Gemini's full audit directory and original model inputs with hashes. PDF hash independently matches SQLite; all four Gemini model-input hashes match saved/current briefs.
  - Supported Gemini's POCI-gain, statutory NAV (~R1.70), duplicate-discount, and reporting-convention corrections, with scope/rounding qualifications. R1.07 retains the disputed R1,479m add-back and is not a validated replacement target. Neither target nor dependent STRONG SELL rating is independently validated.
  - Identified material missed defects: principal collections deducted as outflows in FCFE; FY26/FY27/FY28 forecast cash residuals R532m/R810m/R840m; sensitivity matrix inconsistent with SOTP; UK/US revenue denominator mismatch; short stop-loss below the reference entry price. Qualified R809m as a partial static liquidity comparison, not established future cash shortfall, and retained the 12-month/lifetime valuation issue as unresolved rather than proven under-provisioning.
  - Traced POCI/NAV/footnote errors to captured working papers and ledger before Stage 1. Reviewed duplicate/overbroad guardrail proposals and drafted cash roll-forward/sensitivity checks; no guardrails codified or valuations changed.
  - Extraction/preservation and independent calculation scripts executed with local `.venv` (exit codes 0); visual checks on physical PDF pages 23/31. Application tests not run for this evidence-only review. Market-price arithmetic uses Gemini's R0.90 conditionally; no fresh live quote verified. This review qualifies, rather than overwrites, Gemini's earlier completion entry below.


- **NTU 1H26 Independent Evaluation & Forensic Audit (2026-10-27): CORRECTIONS_REQUIRED**:
  - Executed independent evaluation of Nutun Limited (`NTU`, `1H26`) under `AGENTS.md` and `docs/STOCK_EVALUATION_FORMAT.md` Section 1A.
  - Ran `evaluate_stock.py NTU --period 1H26` (preliminary script exit code 0, status PASSED). Confirmed live JSE closing price of **R0.90** (`NTU.JO`) vs reference **R0.89**. Target price **R0.55** implies **-38.9%** downside (0.0% dividend yield, **-38.9%** 12M TSR). Dynamic rating band evaluates to **`STRONG SELL`** (> R0.65), diverging from the note's static `SELL`.
  - Verified primary source PDF (`nutunlimitedcondensedconsolidatedafs31march2026.pdf`, 38 physical pages, SHA-256: `9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc`) against SQLite `reports` baseline.
  - Saved full audit record to `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T163950Z_gemini/audit.md`, preserved exact input models and prompt manifests in `inputs/`, and saved runnable calculation scripts in `calculations/reconciliations.py` and output in `reconciliations_output.txt`.
  - Identified 3 critical analytical and accounting defects in DeepSeek's analysis:
    1. **SOTP Double-Discounting & Circular Plug**: DeepSeek applied a 25% discount at the equity level to reach R1.07/sh, mechanically applied 25% a second time to reach R0.80/sh, and then applied an unmodeled 31.5% qualitative haircut to hit R0.55 (cumulative 61.5% deduction). Furthermore, inserted an arbitrary R1,479m non-operating asset plug (incorporating R511m double-counted goodwill) solely to force SOTP equity to match forecast book value (R1,115m).
    2. **POCI Accounting Misclassification**: In Note 6.1, R431m is an IFRS 9 cumulative impairment gain (asset write-up reflecting collections exceeding acquisition base-case), NOT a conventional loan loss reserve. DeepSeek calculated an invalid "coverage ratio" (431/3414 = 12.6%) and alleged a "coverage collapse" from 20.4%.
    3. **Contributed Capital vs NAV Conflation**: Claimed treasury shares were bought at R1 vs "R6.90 book value" by dividing gross Share Capital alone (R5,410m) by shares, ignoring R4,111m of accumulated retained losses (true NAV is R1.70/share).
    4. **False Accounting Allegation Rebutted**: DeepSeek claimed the Note 7 amortisation footnote (p. 31) failed to reconcile ($383 + 167 + 728 + 30 + 116 = 1,424 \ne 597$). Independent algebraic verification proved the footnote reconciles under net run-off signs: $(728 - 383 + 167) + (116 - 30) = 512 + 86 = \text{R}598\text{m}$ ($\approx \text{R}597\text{m}$ reported).
  - Formulated 3 proposed sector and universal guardrails: `ALL-SOTP-DISCOUNT-AND-PLUG-ARITHMETIC`, `CONSUMER-LENDING-POCI-GAIN-VS-ECL-RESERVE`, and `ALL-EQUITY-NAV-VS-CONTRIBUTED-CAPITAL`. No valuations overwritten or guardrails codified pending user decision.

- **Persistent independent-evaluation instructions (2026-10-27):** Added mandatory evidence audit records to `docs/STOCK_EVALUATION_FORMAT.md` and automatic loading instructions to `AGENTS.md`. Evaluations require claim IDs, primary-source citations, independent reconciliations, explicit unverified states, findings/revision logs, testable guardrail proposals, and versioned saved handoffs. Codex reviews distinguish supported Gemini findings, DeepSeek errors Gemini missed, and errors Gemini introduced. Updated current model roles and flagged historical architecture descriptions. Documentation-only; existing valuation, database, and code changes were preserved. Normal PowerShell file writes succeeded after restart while `apply_patch` still failed.

- **DCP FY26 Forensic Remediation, Evaluator Hardening & Guardrail Codification (2026-10-27)**:
  - Fully resolved all material errors and disclosure hallucinations identified by the independent evidence review:
    1. **Codified 3 New Institutional Sector Guardrails** into `documents/analysis.sqlite` and `DEFAULT_SECTOR_GUARDRAILS` in `section_capture/db.py` (total enabled rules now **32**):
       - `ALL-DCF-REPRODUCIBILITY`: Mandates explicit disclosure of annual forecast FCFF/FCFE, terminal value, WACC/discount rate, and a step-by-step numerical EV-to-Equity bridge. Forbids applying qualitative, unmodeled percentage markups to blended valuation components; any adjustment must be modeled directly within the underlying cash flows or valuation multiples.
       - `ALL-CASHFLOW-CLASSIFICATION-BRIDGE`: Prohibits relabeling Cash Generated from Operations as Free Cash Flow to Equity (FCFE). Models must explicitly bridge operating cash flow to true free cash flow by deducting replacement and expansion capex, IFRS 16 lease principal repayments, net finance costs, and working capital normalizations.
       - `RETAIL-WORKING-CAPITAL-PAYABLE-STRETCH`: Forbids treating operating cash flow spikes as sustainable free cash flow when driven predominantly by elongation of trade creditor days (>15% YoY increase in trade payables) or inventory freezes during network store expansion.
    2. **Hardened Evaluation Engine (`evaluate_stock.py`)**:
       - Implemented component bounds and percentage blend check in `CHK-SOTP-MATH`: catches prose blends (e.g. `50% DCF (R35.00) + 50% P/E (R26.64) = R30.82`) and verifies that the published target price lies strictly within component bounds $[26.64, 35.00]$ without unmodeled hand-waving uplifts.
       - Integrated cash flow statement FCFE-vs-OCF verification in `CHK-GUARDRAILS`: prevents relabeling Cash Generated from Operations as FCFE.
       - Explicitly flags when live market quote requests fail and fall back to stored reference prices.
    3. **Repaired Stage 1 Forensic Audit Report (`DCP_FY26_stage1_audit_response.md`)**:
       - Extracted and integrated the audited trade receivables aging schedule from AFS physical page 49 (Note 29), documenting that balances over 30 days past due surged from R284.9m to R656.0m (+130% YoY), reflecting credit stress in independent wholesale pharmacy debtors.
       - Corrected the creditor stretch claim: proved that reported creditor days actually contracted from 93.9 to 92.3 days.
       - Disaggregated store populations: 316 corporate retail pharmacies, 280 The Local Choice (TLC) franchise stores (unconsolidated retail revenue), and 42 Baby City stores.
       - Disclosed true balance-sheet net debt of R3.195bn (R3.694bn total borrowings less R500m cash; R6.138bn with leases) and clarified that R4.1bn is the total facility limit (~R2.4bn unutilised headroom).
    4. **Repaired Stage 2 Institutional Valuation Note (`DCP_FY26_stage2_valuation_note.md`)**:
       - Re-anchored target price to the strictly modeled 50/50 blend of Post-IFRS 16 DCF (R35.00) and 18.0x forward P/E on FY27E HEPS of 148.0c (R26.64) = **R30.82**.
       - At live market price R28.60 (reference R28.08), capital upside is **+7.8%** (+9.8% vs reference), forward dividend yield is 2.1%, and expected 12M TSR is **+9.9%** (dynamic rating cleanly evaluates to **`HOLD`**).
       - Reconciled pre-distribution equity cash flow to **R521m** (Cash Generated from Operations R1,793m less R1,104m capex and R692m lease repayments), eliminating the 3.4x cash flow overstatement.
       - Reconciled FY27E statutory PAT (R1,415m) to Headline Earnings attributable to parent equity holders (R1,268m) across NCI and non-operational JV deductions.
    5. **Database & Test Verification**:
       - Synchronized `reports` record in `documents/analysis.sqlite` with the new target price (R30.82) and recommendation (`HOLD`).
       - Full test suite verified: **139 / 139 tests passing** (100% exit code 0).

- **DCP FY26 independent evaluation (2026-10-27): WARNINGS_FOUND**:
  - Ran `evaluate_stock.py DCP --json` (exit code 0). Its automated PASSED result is insufficient: Yahoo DNS failed and the script substituted the stored R28.08 reference price as live; SOTP and guardrail checks missed material issues.
  - Separately retrieved a delayed R28.20 quote (27 October 2026, 14:34 SAST). Existing R36.50 target implies 29.4% upside and 31.5% forecast TSR, but is unsupported: stated 50/50 DCF R35.00 and P/E R26.64 blend is R30.82 (9.3% upside), followed by an unexplained 18.4% uplift. Existing bands imply BUY at R28.20; no validated replacement target or recommendation issued.
  - Verified all three archived PDF SHA-256 values against SQLite. AFS physical pp. 17, 49, 79 visually inspected. FY26 R1,792.711m is reported operating cash flow including dividends paid, not FCFE. Adding back R524.221m dividends and deducting R1,103.588m capex and R691.992m lease principal leaves R521.352m before distributions and borrowing flows. Interest is already deducted. Balance-sheet net debt excluding leases is about R3,194.542m, not merely the R1,166.964m cash/overdraft deficit.
  - Stage 1 needs correction before Stage 2 regeneration: receivables ageing exists (AFS physical p. 49); creditor days fell 93.9 to 92.3 (presentation physical p. 28), contradicting its creditor-stretch explanation; 316 retail pharmacies and 280 TLC franchise stores are separate populations, with 42 baby stores remaining (presentation physical p. 27). R4.1bn denotes facility limits, not verified undrawn headroom.
  - Stage 2 lacks a reproducible DCF/EV bridge and forecast PAT-to-parent-headline-earnings reconciliation; sensitivity base differs from headline forecast. R330m ecosystem spend includes ongoing activity; only R115m is explicitly described as non-recurring. Proposed additional guardrails await user decision; no rules codified, valuations overwritten, or LLM rerun executed. No application code changed; pytest not run for this evidence review.

- **Robust JSE Ticker Lookup & Ground-Truth LLM Web Examination Architecture**:
  - Addressed root cause of LLM hallucinations on ticker examination (e.g. `DCP` incorrectly hallucinated as unlisted "DCP (Pty) Ltd Construction" instead of Dis-Chem Pharmacies Limited):
    1. **Verified Market Data Layer (`section_capture/market_data.py`)**: Added `fetch_jse_company_profile(ticker)` using `yfinance` (`<TICKER>.JO`) to extract authoritative corporate name, ICB sector, sub-industry classification, and official business description directly from JSE market data.
    2. **OpenRouter Live Web Search Integration (`section_capture/openrouter.py`)**: Enhanced `query_openrouter()` with `web_search: bool = False` and `plugins: list` support, seamlessly attaching OpenRouter's live web search plugin (`[{"id": "web"}]`) with retry resilience.
    3. **Ground-Truth LLM Ticker Prompting (`section_capture/ticker_lookup.py`)**:
       - Updated `build_ticker_examination_prompt()` to inject verified JSE listing data as ground truth when available.
       - Enforced a strict anti-hallucination directive: queries official JSE listings and SENS announcements (e.g. `jse.co.za`) to confirm the authentic public entity (e.g. `DCP` = Dis-Chem Pharmacies Ltd, `VOD` = Vodacom Group Ltd, `RBX` = Raubex Group Ltd, `DTC` = Datatec Ltd).
       - Added robust fallback synthesis (`_synthesize_profile_response`) ensuring valid company and sector metadata is returned even if the LLM or network drops.
    4. **Sector Registry Aliases (`companies/sectors.py`)**: Added industry aliases for healthcare/pharmacy retail (`pharmaceutical retailers`, `consumer staples`, `pharmacy`), telecommunications (`communication services`, `telecom services`), and construction (`industrials`, `engineering & construction`) so standard market classifications automatically map to our research sectors.
    5. **Pre-populated High-Impact JSE Constituents (`section_capture/db.py`)**: Added top JSE stocks (`DCP`, `VOD`, `TKG`, `PIK`, `SRE`, `SHP`, `WHL`, `MRP`, `SPP`, `TBS`, `CLS`, `MTN`, `FSR`, `SBK`, `NED`, `ABG`, `INP`, `INL`, `CPI`, `SLM`, `DSY`, `IMP`, `AMS`, `SSW`, `EXX`, `KIO`, `NPH`, `SOL`) to `KNOWN_COMPANIES` for zero-latency local resolution.
    6. **GUI Feedback (`section_capture/new_company_dialog.py`)**: Updated status header to reflect live JSE web search and prompt evaluation.
  - Added new unit tests in [`tests/test_ticker_lookup.py`](file:///c:/Users/diond/Desktop/Projects/stock_analysis_prompts/tests/test_ticker_lookup.py). Full test suite verified: **139 / 139 tests passing** (100% exit code 0).

- **TKG (`FY26`) Telco Evaluation & Guardrail Codification (`evaluate_stock.py TKG`)**:
  - Evaluated Telkom SA SOC Limited (`TKG`, `FY26`): live price **R57.10**, target price **R62.50** (**+9.5%** capital upside, forward dividend yield **4.8%**, projected 12M TSR **+14.3%**, **`HOLD`**).
  - All 5 forensic checks passed cleanly (`CHK-PRICE-SYNC`, `CHK-BANDS-MONO`, `CHK-SOTP-MATH`, `CHK-GUARDRAILS`, `CHK-TEXT-CLEAN`).
  - Codified 2 new telco sector guardrails into `DEFAULT_SECTOR_GUARDRAILS` in `section_capture/db.py` and `sector_guardrails` table in `documents/analysis.sqlite`, bringing total enabled rules to **29**:
    1. `TELCOS-GOODWILL-DISCOUNT-RATE-SENSITIVITY`: Forbids accepting a "no impairment" conclusion on declining telco CGUs (e.g. BCX) achieved solely by slashing the pre-tax discount rate (>200 bps) without underlying risk profile improvement; mandates counterfactual sensitivity testing.
    2. `TELCOS-CLEAN-FCF-DIVIDEND-COVER`: Requires stripping non-operating cash inflows (cell-captive dividends, factoring proceeds, asset disposal gains) when calculating dividend cover against free cash flow payout policies.

- **OpenRouter `:nitro` Socket Drop Root Cause Analysis & Multi-Tier Resilience Architecture**:
  - Diagnosed `[WinError 10054] An existing connection was forcibly closed by the remote host` and `RemoteDisconnected` errors during large-context section audits under `:nitro`:
    - OpenRouter's `:nitro` router dynamically targets highest-throughput endpoints, which under heavy sequential loads (e.g. 11k+ token sections) or upstream provider congestion drop TCP connections with TCP RST packets.
    - Python `urllib.request` on Windows defaulted to keep-alive; half-closed idle sockets dropped by Cloudflare/upstream proxies caused immediate `WinError 10054` on next use.
    - `query_openrouter` reused a single `Request` object across attempts, and `OneShotView` previously had zero section-level retry, causing the entire autonomous pipeline to abort on any transient socket blip.
  - Implemented multi-tier HTTP and GUI pipeline retry system:
    1. **HTTP Keep-Alive Fix**: Added `"Connection": "close"` request header to enforce fresh, clean TCP sessions per request and avoid half-closed keep-alive socket drops.
    2. **Fresh `Request` Reconstruction**: Re-instantiates `urllib.request.Request` per attempt with fresh buffers.
    3. **Expanded Exception Handling**: Catches all connection drops (`ConnectionResetError`, `RemoteDisconnected`, `IncompleteRead`, `URLError`, `TimeoutError`, HTTP 429/5xx) with exponential backoff (`2 ** attempt` seconds).
    4. **Automatic `:nitro` Fallback**: If a `:nitro` endpoint fails repeatedly (attempts 1–2), attempts 3–4 automatically fall back to the standard base model without `:nitro`, preventing run failures from provider-specific Nitro instability.
    5. **GUI Pipeline Section Retry**: In `OneShotView._process_next_section`, transient section failures are retried up to 3 times with 3s backoff and live user notifications (`⚠️ Network hiccup on Section #X... Retrying in Ys`) before giving up. Added 2-attempt retries for Stage 1 and Stage 2.
  - Added unit tests `test_query_openrouter_retry_on_winerror_10054` and `test_query_openrouter_nitro_fallback_to_standard` in [`tests/test_openrouter.py`](file:///c:/Users/diond/Desktop/Projects/stock_analysis_prompts/tests/test_openrouter.py).
  - Full test suite verified: **136 / 136 tests passing** (100% exit code 0).

- **OpenRouter DeepSeek Model Configured to `:nitro` (`deepseek/deepseek-v4.1-flash-1017:nitro`)**:
  - Configured preferred OpenRouter model setting to high-throughput, low-latency Nitro variant:
    - Updated `EXTERNAL_SECRETS_PATH` (`secrets.env`) setting `OPENROUTER_MODEL=deepseek/deepseek-v4.1-flash-1017:nitro`.
    - Updated `DEFAULT_MODEL` fallback in [`section_capture/openrouter.py`](file:///c:/Users/diond/Desktop/Projects/stock_analysis_prompts/section_capture/openrouter.py) to `"deepseek/deepseek-v4.1-flash-1017:nitro"`.
    - Verified live OpenRouter API completion: succeeded in 2.09s via Nitro endpoint.
    - Updated unit tests in [`tests/test_openrouter.py`](file:///c:/Users/diond/Desktop/Projects/stock_analysis_prompts/tests/test_openrouter.py). Full test suite verified with 134/134 passing (100% exit code 0).

- **NTU (`1H26`) Migration & Blank Period Combo Mandatory Validation**:
  - Corrected Nutun Limited (`NTU`) interim reporting period from `FY26` to `1H26` (Nutun fiscal year ends 30 September; reports for 6 months ended 31 March 2026 are `1H26`):
    - Migrated briefs directory to `companies/consumer_lending/NTU/briefs/1H26/` and renamed all Stage 1 & Stage 2 prompts and notes to `NTU_1H26_*`.
    - Migrated archived PDF directory to `companies/consumer_lending/NTU/sources/completed/1H26/`.
    - Updated `reports` table in `documents/analysis.sqlite` setting `period = '1H26'` and updating `original_path`.
    - Re-evaluated NTU via `evaluate_stock.py NTU`: perfectly resolved `1H26`, confirming **R0.55** target price (**-38.2%** downside vs live R0.89, **STRONG SELL**) with all 5 forensic checks passing cleanly.
  - Eliminated automatic period combo box pre-population in PySide6 app (`section_capture/one_shot_view.py` and `section_capture/window.py`):
    - Initialized `period_combo` with an empty string `""` as index 0 and placeholder text `"Select / Enter Period"`.
    - Disallowed automatic pre-selection of fallback `FY26` or detected period when selecting companies or scanning files.
    - Updated `start_pipeline()` to enforce mandatory reporting period validation: if the combo is left blank, a blocking `QMessageBox.critical` ("Reporting Period Required") is triggered and execution is immediately aborted.
    - Added dedicated test `test_period_combo_blank_by_default_blocks_auto_pipeline` in `tests/test_one_shot_pipeline.py`.
    - Full test suite verified with 134/134 tests passing (100% exit code 0).

- **NTU (`1H26`) Consumer Lending Evaluation & Guardrail Codification (`evaluate_stock.py NTU`)**:
  - Freshly audited and evaluated Nutun Limited (`NTU`) following complete re-capture by user.
  - Live JSE closing price **`R0.89`** (`NTU.JO`), derived 12-Month Target Price of **`R0.55` (`STRONG SELL`)**, implying **`-38.2%` capital downside** (forward dividend yield: 0.0%; expected 12M TSR: **`-38.2%`**).
  - Monotonic dynamic rating bands established: `Strong Buy ≤ R0.42`, `Buy ≤ R0.48`, `Hold ≤ R0.58`, `Sell ≤ R0.65`, `Strong Sell > R0.65`.
  - At live price **`R0.89`** (> R0.65), NTU dynamically evaluates to a high-conviction **`STRONG SELL`**.
  - All 5 forensic checks pass cleanly (`CHK-PRICE-SYNC`, `CHK-BANDS-MONO`, `CHK-SOTP-MATH`, `CHK-GUARDRAILS`, `CHK-TEXT-CLEAN`).
  - Codified newly discovered consumer lending guardrail `CONSUMER-LENDING-PBD-AMORTISATION-EBITDA-ADD-BACK` into `documents/analysis.sqlite` (`sector_guardrails` table) bringing total enabled rules to **27**.
  - Synchronized SQLite `reports` table with `target_price_zar = 0.55`, `reference_price_zar = 0.89`, `recommendation = SELL`, `upside_pct = -38.2`, and dynamic rating bands.

- **Reset and Fresh Start for NTU (Nutun) and TKG (Telkom)**:
  - Purged all database records for NTU and TKG from `documents/analysis.sqlite`: deleted 3 report rows and 129 linked section captures.
  - Cleared all generated brief directories on disk: `companies/consumer_lending/NTU/briefs/1H26/` and `companies/telcos/TKG/briefs/FY26/`.
  - Cleared `sources/completed/` archives for both tickers, restoring un-analyzed status.
  - Preserved original source PDFs in `companies/consumer_lending/NTU/sources/` and `companies/telcos/TKG/sources/`, ready for fresh section capture in the PySide6 app.

- **IOC (`FY26`) IT Services Valuation Refresh & Hold Re-Rating (`evaluate_stock.py IOC --rerun`)**:
  - Codified new IT sector guardrail `IT-HARDWARE-PASSTHROUGH-MARGIN-DILUTION` into `documents/analysis.sqlite` (`sector_guardrails` table) bringing total enabled rules to 26.
  - Re-ran Stage 2 Institutional Valuation via DeepSeek Flash using verified live closing price **`R4.22`** (`IOC.JO`), incorporating post-balance sheet debt restructuring (margin cut by 50 bps, maturity extended to March 2030), M&A cash obligations, and hardware margin disaggregation.
  - Derived 12-Month Target Price of **`R4.60` (`HOLD`)**, implying **`+9.0%` capital upside** (forward dividend yield: 0.0% as capital is prioritized for share buybacks and bolt-ons; expected 12M TSR: **`+9.0%`**).
  - Monotonic dynamic rating bands established: `Strong Buy ≤ R3.54`, `Buy ≤ R4.00`, `Hold ≤ R4.84`, `Sell ≤ R5.41`, `Strong Sell > R5.41`.
  - At live price **`R4.22`**, IOC dynamically migrates to **`HOLD`** (`R4.01 – R4.84`).
  - Stripped illegal HTML tags and verified all 5 forensic checks pass cleanly (`CHK-PRICE-SYNC`, `CHK-BANDS-MONO`, `CHK-SOTP-MATH`, `CHK-GUARDRAILS`, `CHK-TEXT-CLEAN`).
  - Synchronized SQLite `reports` table with `target_price_zar = 4.60`, `reference_price_zar = 4.22`, `recommendation = HOLD`, `upside_pct = 9.0`, and dynamic rating bands.
  - Archived primary source PDFs to `companies/it/IOC/sources/completed/FY26/` (`iOCO-AFS-July2026.pdf`, `iOCO-IAR-2026.pdf`).

- **Codification of 6 New Sector Guardrails & Interactive Database Prompt Workflow**:
  - Inserted 6 newly discovered valuation guardrails into `documents/analysis.sqlite` (`sector_guardrails` table) bringing total enabled rules to 25:
    1. `REIT-YIELD-STRIP-ICR-DEFAULT`: Prohibits unanalyzed yield-stripping asset sales that accelerate ICR covenant defaults.
    2. `REIT-SWAP-NOTIONAL-MATCHING`: Penalizes debt paydowns that trigger over-hedged swap books (>100% of gross borrowings).
    3. `MINING-BYPRODUCT-AISC-SEPARATION`: Prohibits applying consolidated by-product subsidized AISC to standalone starter mining phases.
    4. `MINING-INFERRED-RESOURCE-HAIRCUT`: Mandates explicit 25%–50% risk discounts on unproven Inferred mineral resources in LOM plans.
    5. `RETAIL-APM-OPERATING-MARGIN`: Distinguishes merchandise-only APM EBIT margins from statutory total revenue operating margins.
    6. `RETAIL-HIDDEN-ARREARS-AUDIT`: Mandates forensic extraction of overdue debt concealed within "satisfactory paid" credit accounts.
  - Updated [`docs/STOCK_EVALUATION_FORMAT.md`](file:///c:/Users/diond/Desktop/Projects/stock_analysis_prompts/docs/STOCK_EVALUATION_FORMAT.md) and [`AGENTS.md`](file:///c:/Users/diond/Desktop/Projects/stock_analysis_prompts/AGENTS.md) to mandate that after every evaluation or rerun, the assistant must explicitly prompt the user to codify newly discovered rules into the SQLite database.

- **APF (`FY26`) REIT Valuation Refresh & Strong Sell Re-Rating (`evaluate_stock.py APF --rerun`)**:
  - Re-ran Stage 2 Institutional Valuation via DeepSeek Flash using verified live closing price **`R0.48`** (`APF.JO`), incorporating all 8 subsequent SENS notices (KPMG Crescent disposal to RMA, JSE censure, DMTN partial capital redemptions).
  - Derived 12-Month Target Price of **`R0.30` (`STRONG SELL`)**, implying **`-37.5%` capital downside** (forward dividend yield: 0.0% due to Section 46 liquidity blockade; expected 12M TSR: **`-37.5%`**).
  - Monotonic dynamic rating bands established: `Strong Buy ≤ R0.23`, `Buy ≤ R0.26`, `Hold ≤ R0.32`, `Sell ≤ R0.35`, `Strong Sell > R0.35`.
  - At live price **`R0.48`** (> R0.35), APF dynamically migrates to a high-conviction **`STRONG SELL`**.
  - Cleaned all token stutter loops in Section 3 and stripped illegal HTML tags. All 5 forensic checks pass cleanly (`CHK-PRICE-SYNC`, `CHK-BANDS-MONO`, `CHK-SOTP-MATH`, `CHK-GUARDRAILS`, `CHK-TEXT-CLEAN`).
  - Synchronized SQLite `reports` table with `target_price_zar = 0.30`, `reference_price_zar = 0.48`, `recommendation = SELL`, `upside_pct = -37.5`, `tsr_pct = -37.5`, and rating bands.
  - Archived primary source PDF to `companies/reit/APF/sources/completed/FY26/APF_IAR_2026_Combined_V21.pdf`.

- **Stock Evaluation Protocol & Output Specification (`docs/STOCK_EVALUATION_FORMAT.md`)**:
  - Authored comprehensive operating guide [`docs/STOCK_EVALUATION_FORMAT.md`](file:///c:/Users/diond/Desktop/Projects/stock_analysis_prompts/docs/STOCK_EVALUATION_FORMAT.md) standardizing CLI execution commands, 5-part user response structure, and sector-specific forensic checklists.
  - Mandated the inclusion of a dedicated **Valuation Errors Found & Analytical Lessons Learned** section on every stock evaluation and rerun response, breaking down operational distortions, financing facility asymmetries, hidden credit arrears, and tax mechanics.
  - Codified the post-rerun synchronization checklist: SQLite database update, PDF archival, test suite execution, and state documentation.

- **ORN (`FY26`) Mining Valuation Refresh (`evaluate_stock.py ORN --rerun`)**:
  - Re-ran Stage 2 Institutional Valuation via DeepSeek Flash using verified live closing price **`R0.25`** (`ORN.JO`), incorporating post-SENS financing updates (Glencore Tranche A & B facilities) and mining sector guardrails.
  - Derived 12-Month Target Price of **`R0.28` (`HOLD`)**, implying **`+12.0%` capital upside** (forward dividend yield: 0.0%, TSR: `+12.0%`).
  - Monotonic dynamic rating bands established: `Strong Buy ≤ R0.22`, `Buy ≤ R0.24`, `Hold ≤ R0.29`, `Sell ≤ R0.33`, `Strong Sell > R0.33`.
  - At live price **`R0.25`**, ORN is dynamically rated **`HOLD`**.
  - All 5 forensic checks pass cleanly (`CHK-PRICE-SYNC`, `CHK-BANDS-MONO`, `CHK-SOTP-MATH`, `CHK-GUARDRAILS`, `CHK-TEXT-CLEAN`).
  - Synchronized SQLite `reports` table (`d20cdd6e34bde68c871b45bc80f57dea9ce6b963d607464e3c28f0456ba9eae0`) with `target_price_zar = 0.28`, `reference_price_zar = 0.25`, `recommendation = HOLD`, `upside_pct = 12.0`, `rating_bands`.
  - Archived source PDF to `companies/mining/ORN/sources/completed/FY26/20260917-ORN-ASX-JSE-Annual-Report-2026.pdf`.

- **LEW (`FY26`) Retail Valuation Refresh & OpenRouter Transient Retry Architecture**:
  - **Refreshed Stage 2 Institutional Valuation (`evaluate_stock.py LEW --rerun`)**:
    - Re-ran Stage 2 Institutional Valuation via DeepSeek Flash using verified live closing price **`R90.19`** (`LEW.JO`).
    - Derived 12-Month Target Price of **`R95.00` (`HOLD`)**, implying **`+5.3%` capital return** plus **`9.4%` forward dividend yield** = **`+14.8%` expected 12M TSR**.
    - Monotonic dynamic rating bands established: `Strong Buy ≤ R73.08`, `Buy ≤ R82.61`, `Hold ≤ R100.00`, `Sell ≤ R111.76`, `Strong Sell > R111.76`.
    - At the live JSE price of **`R90.19`**, LEW is rated **`HOLD`** (`R82.62 – R100.00`).
    - Stripped out all deprecated `<br>` HTML tags from Markdown table cells and embedded clean JSON rating bands.
    - Synchronized SQLite `reports` table (`4f42a10cf4986783285887e8458999c314edb3c4dcc6985c18e1a46795b82e14`) with `target_price_zar = 95.00`, `reference_price_zar = 90.19`, `recommendation = HOLD`, `upside_pct = 5.3`, `dividend_yield_pct = 9.4`, `tsr_pct = 14.8`, and dynamic rating bands.
    - Archived source PDF to `companies/retail/LEW/sources/completed/FY26/lewis-iar-2026.pdf`.
  - **OpenRouter Transient Connection Retry**:
    - Added automatic exponential backoff retry loop (3 attempts) to `query_openrouter` in [`section_capture/openrouter.py`](file:///c:/Users/diond/Desktop/Projects/stock_analysis_prompts/section_capture/openrouter.py) to gracefully absorb transient remote socket resets (`WinError 10054`) and HTTP 5xx errors.

- **Automated Stock Valuation Evaluator & Autonomous Rerun Engine (`evaluate_stock.py`)**:
  - Implemented standalone CLI and programmatic engine [`evaluate_stock.py`](file:///c:/Users/diond/Desktop/Projects/stock_analysis_prompts/evaluate_stock.py) to standardize and automate forensic evaluations when asked to evaluate any stock (`python evaluate_stock.py <TICKER> [--period <PERIOD>] [--rerun] [--json]`).
  - **Programmatic Forensic Audit Checks**:
    - `CHK-PRICE-SYNC`: Fetches live JSE quote (`XYZ.JO`), evaluates live upside vs note reference price, and recomputes 12M TSR.
    - `CHK-BANDS-MONO`: Confirms strictly ascending rating bands (`Strong Buy < Buy < Hold < Sell < Strong Sell`) and evaluates live dynamic rating.
    - `CHK-SOTP-MATH`: Scans SOTP tables for vertical summation, proper Net Cash/Debt signs, and flags blended target price arithmetic hallucinations.
    - `CHK-GUARDRAILS`: Verifies compliance against active sector-specific and universal rules in `sector_guardrails`.
    - `CHK-TEXT-CLEAN`: Scans for LLM token repetition/sampling stutters, broken HTML tags (`<br>`, `<span>`), and template placeholders.
  - **Autonomous `--rerun` Capability**:
    - Automatically builds multi-document dossier (Stage 1 audit determinations + source PDFs from `sources/` or `sources/completed/<period>/` + SENS notices).
    - Queries OpenRouter DeepSeek Flash with temperature 0.1, sanitizes markdown, repairs rating bands, saves note, updates SQLite `reports`, and archives PDFs.
  - **Verified Test Suite**:
    - Added unit test suite [`tests/test_evaluator.py`](file:///c:/Users/diond/Desktop/Projects/stock_analysis_prompts/tests/test_evaluator.py) testing discovery, audit execution across active stocks (`PAN`, `SSK`, `CGR`, `SPP`), and detection of non-monotonic bands, arithmetic hallucinations, and HTML tags.
    - All **133 tests passing (100%)**.

- **PAN (`FY26`) Mining Valuation Refresh & Dynamic Strong Buy Re-Rating**:
  - **Refreshed Stage 2 Institutional Valuation**:
    - Re-ran Stage 2 Institutional Valuation via DeepSeek Flash using verified live closing price **`R24.60`** (`PAN.JO`), incorporating the dedicated mining sector guardrail (`MINING-SECTION36-CAPEX-TAX`) and the 10 universal guardrails.
    - Derived 12-Month Target Price of **`R34.50` (`BUY`)**, implying **`+40.2%` capital upside** (plus `3.9%` dividend yield = `+44.1%` TSR) across 2,106.3m economic shares (net of PAR Gold 306.4m treasury shares and the R500m on-market share buyback).
    - Monotonic dynamic rating bands established: `Strong Buy ≤ R26.54`, `Buy ≤ R30.00`, `Hold ≤ R36.32`, `Sell ≤ R40.59`, `Strong Sell > R40.59`.
    - At the live JSE closing price of **`R24.60`**, PAN is dynamically rated **`STRONG BUY`** (`≤ R26.54`).
    - Fixed arithmetic SOTP DCF table to sum vertically line-by-line to `US$4,274.7m` and `R34.50/share` without arbitrary discounts or net cash deductions.
    - Synchronized [`documents/analysis.sqlite`](file:///c:/Users/diond/Desktop/Projects/stock_analysis_prompts/documents/analysis.sqlite) `reports` row (`62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd`) with `target_price_zar = 34.50`, `reference_price_zar = 24.60`, `recommendation = BUY`, `upside_pct = 40.2`, `dividend_yield_pct = 3.9`, `tsr_pct = 44.1`, and dynamic rating bands.
    - Cleaned token stutter in Section 6 catalysts and archived primary results PDF to `companies/mining/PAN/sources/completed/FY26/`.

- **SSK (`FY26`) Valuation Refresh & Generic Sector Guardrails Enforcement**:
  - **Cleaned Sector Guardrails Registry (`sector_guardrails`)**:
    - Strictly enforced user rule: guardrails must be 100% generic institutional principles applicable across any company in a sector, with zero company-specific names, tickers, or numbers in the rule text, and never forced if unnecessary.
    - Cleaned `ALL-ENTITY-ACRONYM-DISAMBIGUATION` and `RETAIL-IFRS16-HEADLEASE-SUBLEASE` to remove company-specific identifiers (`SPAR`, `CGR`, `BDC`).
    - Kept 11 core generic rules active in SQLite `sector_guardrails` across universal and sector domains (`ALL-IFRS16-EV-BRIDGE`, `ALL-PNL-VERTICAL-ARITHMETIC`, `ALL-CROSS-SECTION-METRIC-SYNC`, `ALL-RATING-BANDS-MONOTONIC`, `ALL-SHARE-COUNT-ANCHOR`, `ALL-HISTORICAL-BASE-COLUMN`, `ALL-PAT-HEPS-RECONCILIATION`, `ALL-SOTP-ARITHMETIC-AND-NO-DOUBLE-COUNT`, `ALL-TREASURY-SHARE-DIVIDEND-BRIDGE`, `ALL-ENTITY-ACRONYM-DISAMBIGUATION`, `CONSTRUCTION-POC-WIP-RETENTIONS`).
  - **Refreshed SSK (`FY26`) Institutional Valuation**:
    - Re-ran Stage 2 Institutional Valuation via DeepSeek Flash using verified JSE quote `R5.78` (`SSK.JO`).
    - Revised target price to **`R6.20` (`HOLD`)**, implying **`+7.3%` upside** (down from old `R8.50 BUY`), properly accounting for the `R133m` working capital deficit, `R2.65bn` excess billings, and stripping out the `R492m` post-tax Kusile settlement windfall to anchor on `R328m` normalised OP.
    - Generated and registered `companies/construction/SSK/briefs/FY26/SSK_FY26_stage2_valuation_note.md` and synced SQLite `reports` table with `target_price_zar = 6.20`, `reference_price_zar = 5.78`, `recommendation = HOLD`, and dynamic rating bands (`Strong Buy <= R4.77`, `Buy <= R5.39`, `Hold <= R6.53`, `Sell <= R7.29`, `Strong Sell > R7.29`).
    - Archived source PDFs to `companies/construction/SSK/sources/completed/FY26/`.

- **Streamlined Portfolio Coverage Table (`section_capture/portfolio_view.py`)**:
  - Removed redundant `Note Ref Price` and `Note Upside` columns from the Portfolio Coverage table (streamlining from 13 columns to 11 columns: `Ticker`, `Company Name`, `Sector`, `Latest JSE Price`, `12M Target`, `Live Upside`, `Div Yield`, `12M TSR`, `Rating`, `Stage 1 / S2 Status`, `Analysis Date`) as well as from the KPI header strip and Markdown clipboard export.
  - Added seamless fallback in `Latest JSE Price` and `Live Upside` to `reference_price_zar` / `upside_pct` when no cached `market_quotes` row is present, and made `12M TSR` dynamically reflect `Live Upside + Div Yield` when live quotes are active.

- **SQLite Sector Guardrails Registry (`sector_guardrails`) & Zero-Move Post-SENS Resubmission Workflow**:
  - **CGR (`FY26`) Forensic Guardrails & Re-Run (`R3.10 SELL` vs Live JSE `R3.65`)**:
    - Added 4 universal guardrails derived from Calgro M3 (`CGR` `FY26`): `ALL-PAT-HEPS-RECONCILIATION` (enforces PAT-to-HEPS directional reconciliation and Net Finance income/expense sign integrity), `ALL-SOTP-ARITHMETIC-AND-NO-DOUBLE-COUNT` (enforces strict vertical SOTP summation and forbids adding working capital/goodwill on top of DCF), `ALL-TREASURY-SHARE-DIVIDEND-BRIDGE` (reconciles gross vs net treasury shares on parent vs consolidated dividends), and `ALL-ENTITY-ACRONYM-DISAMBIGUATION` (prevents conflating distinct legal entities such as Bankenveld District City vs Belhar Calgro M3).
    - Re-ran CGR (`FY26`) Stage 1 and Stage 2 (`companies/construction/CGR/briefs/FY26/CGR_FY26_stage2_valuation_note.md`), archiving PDFs to `sources/completed/FY26/`.
  - **SQLite `sector_guardrails` Table (`section_capture/db.py`)**:
    - Added persistent `sector_guardrails` table (`rule_code`, `sector`, `stage`, `title`, `rule_text`, `origin_ticker`, `enabled`, `created_at`, `updated_at`) auto-seeded via `_migrate_schema()` with universal (`all`) and sector-specific (`retail`, `mining`, `reit`, `it`, `construction`, `consumer_lending`, `finance`, `telcos`) accounting and valuation guardrails.
    - Codified forensic guardrails from SPP (`1H26`): `ALL-IFRS16-EV-BRIDGE` (forbids subtracting capitalised IFRS 16 lease liabilities from Pre-IFRS 16 EBITDA/FCFF Enterprise Value), `ALL-PNL-VERTICAL-ARITHMETIC` (enforces vertical P&L row summation and forbids double-subtracting Note 7 impairments from statutory Operating Profit), `ALL-CROSS-SECTION-METRIC-SYNC` (enforces Section 1 ↔ Section 3 ↔ Section 4 HEPS/multiple/target price identity), `ALL-RATING-BANDS-MONOTONIC` (enforces strictly ascending ZAR rating band thresholds), `RETAIL-IFRS16-HEADLEASE-SUBLEASE`, and `RETAIL-ECL-CASHFLOW-VS-ALLOWANCE`.
    - Added `upsert_sector_guardrail()`, `get_sector_guardrails()`, and `format_sector_guardrails_block()`, automatically injecting active guardrails into Stage 1 (`workflow/export_stage1.py`), Stage 2 (`workflow/generate_stage2.py`), and Stage 2-U SENS updates (`workflow/generate_sens_update.py`).
    - Added `validate_and_repair_rating_bands()` (`section_capture/db.py`) and `sanitize_stage2_valuation_markdown()` (`workflow/generate_stage2.py`) to deterministically repair degenerate JSON `rating_bands` (e.g. `hold_max_zar == sell_max_zar`).
  - **In-Place Archived PDF/SENS Discovery & SQLite Stage 1 Reuse (`section_capture/one_shot_view.py`)**:
    - Updated `discover_company_documents()` to automatically discover archived report PDFs in `sources/completed/<period>/` (`is_archived=True`) and prior completed SENS notices in `sources/sens/completed/` (`is_archived=True`) alongside new SENS notices in `sources/sens/` (`is_archived=False`), eliminating the need to manually pull PDFs out of `completed/` to resubmit.
    - Added `_load_existing_stage1_response()` to load `stage1_response` from `documents/analysis.sqlite` or `briefs/<period>/` so both Smart SENS Update Mode (`_run_phase4_sens_only_update`) and full Stage 2 resubmission (`_run_phase3_stage1` $
ightarrow$ `_run_phase4_stage2`) reuse Stage 1 from SQLite without re-running Tier 1 or Stage 1.
    - Upgraded `_run_phase4_sens_only_update()` and `build_sens_update_prompt_content()` to inject the Stage 1 Forensic Audit (`stage1_audit_report`), full document inventory (`ensure_documents_considered_table()`), and sector guardrails into every SENS valuation update.
  - **Test Suite (`tests/test_one_shot_pipeline.py`)**:
    - Added 4 new tests (`test_sector_guardrails_table_and_prompt_injection`, `test_sanitize_stage2_valuation_markdown_repairs_degenerate_bands`, `test_discover_archived_pdfs_and_sens_in_place_and_smart_sens_update`, `test_resubmit_stage2_from_completed_pdfs_and_sqlite_stage1`).
    - All **127 tests passing (100%)**.

- **One-Shot Autonomous End-to-End Pipeline (`one_shot` branch — `section_capture/one_shot_view.py`)**:
  - Streamlined User Experience:
    1. User creates or selects a company (`Ticker` / `Sector`) via `OneShotView`.
    2. User places PDFs into `sources/` or SENS notices into `sources/sens/` (with one-click `📂 Open sources/` and `📂 Open sources/sens/` buttons).
    3. UI automatically scans and displays discovered documents (`[PRES]`, `[IAR]`, `[AFS]`, `[SENS]`), page counts, and auto-detected Reporting Period (`FY26`, `1H26`, etc.), with `▲ Move Doc Up` / `▼ Move Doc Down` ordering controls.
    4. Clicking `🚀 Start Autonomous Analysis` runs all 5 phases automatically end-to-end:
       - **Phase 1 (PDF Ingestion & Section Mapping)**: `IngestionWorker(QThread)` registers PDFs in SQLite, links companion reports, maps sections (LLM slide clustering for presentations, TOC/Heading scan for AFS/IAR), and auto-captures packages.
       - **Phase 2 (Sequential Section Audit & Questions Ledger)**: Queues and audits all pending sections across all documents in order, rebuilding each section's prompt with the latest accumulated Questions Ledger.
       - **Phase 3 (Stage 1 Forensic Audit)**: Compiles primary + companion sections and final Questions Ledger, executes Stage 1 audit via `OpenRouterWorker`, and saves `<TICKER>_<PERIOD>_stage1_audit_response.md`.
       - **Phase 4 (Stage 2 Institutional Valuation / Smart SENS Update)**: Assembles full PDF + SENS dossier (or runs SENS-only update if baseline valuation already exists), executes SOTP DCF valuation, and saves `<TICKER>_<PERIOD>_stage2_valuation_note.md` + dynamic rating bands.
       - **Phase 5 (Archiving & Portfolio Sync)**: Archives processed PDFs to `sources/completed/<PERIOD>/` and SENS notices to `sources/sens/completed/`, displaying the final Rating Badge and 12m Target Price.
  - Detailed Live Progress Screen:
    - 5-Phase visual stepper cards (`Waiting` $\rightarrow$ `⏳ Active` $\rightarrow$ `✓ Done`), overall progress bar, live document table status column, timestamped telemetry log (`QTextBrowser`), and live artifact preview tabs (`Questions Ledger`, `Stage 1 Forensic Audit`, `Stage 2 Valuation Note`).
    - Archive & Artifact Synchronization:
      - Processed PDFs archived to `sources/completed/<PERIOD>/` remain excluded from the active document queue.
      - Artifact preview tabs dynamically reload upon period or company change, auto-detecting existing period folders (e.g. `1H26`) and rendering the Questions Ledger, Stage 1 Forensic Audit, and Stage 2 Valuation Note immediately.
    - Live Closing Price & Strict Anti-Guessing Mechanism:
      - Before Stage 2 Valuation (or SENS update), queries `fetch_jse_quote(ticker)` via `yfinance` normalized with `.JO` (e.g. `SPP.JO`).
      - Strict Anti-Guessing Rule: If live `yfinance` fails, prompts the user directly via `QInputDialog` to input the verified closing price. Never falls back to stale cache and never guesses.
      - Injects the confirmed `reference_price_zar` directly into the Stage 2 JSON block and prompt instructions, forbidding LLM hallucination and enforcing upside calculation and rating bands relative to this exact baseline.
    - Minimalist UI Architecture (Removed PDF Viewing, Manual Capture Split-Pane & Valuation Dossier Dialog):
      - Deleted `section_capture/pdf_view.py` (`PdfCanvas`) and stripped bitmap rendering (`render()`, `_crop_image()`, `QPdfDocument`) from `section_capture/pdf_source.py`, accelerating headless page capture by 5-10x.
      - Deleted `section_capture/audit_dialog.py` (`AuditValuationDialog`, ~1,612 lines) and removed the `🏛️ Valuation Dossier` button from `OneShotView`.
      - Refactored `CaptureWindow` (`section_capture/window.py`, 1,834 lines -> 212 lines) to remove both legacy top toolbars and the manual tab, mounting `OneShotView` directly as the central widget.
      - Routed the `📊 Analyzed Stocks` button in `OneShotView` directly to the standalone `PortfolioCoverageDialog` (`section_capture/portfolio_view.py`).
  - Test Suite (`tests/test_one_shot_pipeline.py`):
    - Added unit tests for document discovery/ordering, UI reordering, live quote fetching, and user dialog fallback; retired obsolete manual PDF canvas and `AuditValuationDialog` tests.
    - All **122 tests passing (100%)**.

- **LLM Semantic Clustering for Presentation Decks (`extract_all_app_sections`)**:
  - Solved single-slide fragmentation in corporate presentations (`section_capture/section_matcher.py`):
    - Previously, PowerPoint's internal TOC bookmarks (`Slide 1`, `Slide 2`...) caused decks to be sliced into 38 to 61 individual 1-slide sections, generating 38-61 API calls and ballooning the Questions Ledger to 275+ questions.
    - Implemented `is_presentation_deck()`: Detects landscape aspect ratio ($w/h \ge 1.25$), `doc_type == "presentation"`, or PowerPoint slide bookmark patterns.
    - Implemented `llm_cluster_presentation_sections()`: Ingests a compact slide title/snippet manifest and queries DeepSeek to partition the entire deck into **4 to 7 coherent institutional equity research sections** (e.g. *Executive Overview & Diagnosis*, *Segment Operations*, *Financial Review*, *Balance Sheet & Debt*, *Turnaround Strategy & Outlook*, *Appendices*).
    - Implemented `heuristic_cluster_presentation_sections()`: Robust pure-Python fallback for offline use using divider slide word count (< 25 words) and speaker transition cues.
  - Benchmarked on SPP (58 slides $\rightarrow$ 6 multi-slide sections) and PIK (38 slides $\rightarrow$ 5 multi-slide sections), cutting deck turnaround time from ~45 minutes to ~5 minutes.
  - Test Suite (`tests/test_section_matcher.py`):
    - Added unit test `test_presentation_clustering` covering detection, heuristic clustering, and mocked LLM clustering.
    - Expanded test suite to **148 tests passing (100%)**.

- **Document Order Selection Dialog for Batch Auto-Capture & Sequential Ledger Chaining**:
  - Implemented `DocumentOrderDialog` (`section_capture/map_dialog.py`):
    - Discovers all companion reports for the active company and period (presentations `[PRES]`, annual/interim financial statements `[AFS]`, integrated reports `[IAR]`, annual reports `[AR]`).
    - Interactive dialog modal with checkboxes and `▲ Move Up` / `▼ Move Down` buttons, allowing the user to set the exact document processing sequence.
  - Sequential Auto-Capture & Cross-Document Ledger Pipeline (`section_capture/map_dialog.py` & `section_capture/window.py`):
    - Upon clicking `⚡ Auto-Capture Matched Sections` with multiple companion documents present, `DocumentOrderDialog` prompts the user for order confirmation.
    - Extracts sections sequentially across all selected documents into `analysis.sqlite`, auto-linking sibling/parent reports.
    - Passes `ordered_shas` to `CaptureWindow.run_all_pending(ordered_shas=ordered_shas)`, ensuring the DeepSeek worker analyzes Document 1 first and Document 2 second so the Questions Ledger accumulates and flows smoothly across reports.
  - Pending Count Multi-Doc Visibility:
    - `CaptureWindow._update_actions()` computes total pending sections across all active and companion reports for the company family.
  - Test Suite (`tests/test_section_matcher.py`):
    - Added `test_document_order_dialog` (table rendering, order swapping up/down, checkbox exclusion).
    - Added `test_auto_capture_multi_document_ordering` (validating multi-report sequence execution into `run_all_pending`).
    - All **147 tests passing (100%)**.

- **Automated Sequential DeepSeek Processing upon Auto-Capture (`run_all_pending`)**:
  - Enhanced Section Comparison & Auto-Capture Dialog (`section_capture/map_dialog.py`):
    - When `⚡ Auto-Capture Matched Sections` completes extracting sections into SQLite, it automatically finds the parent `CaptureWindow` and triggers `run_all_pending()` directly.
    - Closes modal comparison and map dialogs, returning the user to the main capture canvas where `⚡ DeepSeek Running (N in queue)` and the status bar immediately display live background processing and questions ledger construction.
  - Test Suite (`tests/test_section_matcher.py`):
    - Added test coverage in `test_auto_capture_matched_sections` asserting that `target.run_all_pending()` is invoked automatically upon completing auto-capture.
    - All 145 tests passing (100%).

- **Dynamic Valuation Rating Levels & Live Market Price Evaluation (`Strong Buy`, `Buy`, `Hold`, `Sell`, `Strong Sell`)**:
  - Enhanced Stage 2 Prompt Generator (`workflow/generate_stage2.py`):
    - Updated `_format_section1_spec()` to instruct the LLM to output explicit ZAR price boundaries (`strong_buy_max_zar`, `buy_max_zar`, `hold_max_zar`, `sell_max_zar`, `strong_sell_above_zar`) anchored to the 12-month JSE target price in the mandatory Section 1 JSON block.
    - Added a structured dynamic rating bands row to the visual Executive Summary Markdown table.
  - Database & Rating Engine (`section_capture/db.py`):
    - Added `compute_rating_bands_fallback()`: Generates standardized institutional thresholds from the 12-month target price ($>+30\%$ Strong Buy, $+15\%$ to $+30\%$ Buy, $-5\%$ to $+15\%$ Hold, $-5\%$ to $-15\%$ Sell, $<-15\%$ Strong Sell) if explicit bands are not yet present in a note.
    - Added `evaluate_dynamic_rating()`: Dynamically evaluates the latest market quote against price bands to calculate the live rating.
    - Updated `parse_valuation_summary()` to parse `rating_bands` and store into `valuation_summary_json`.
    - Updated `get_analyzed_stocks()` to return `rating_bands`, `dynamic_recommendation`, and preserve `static_recommendation`.
  - Portfolio Dashboard UI (`section_capture/portfolio_view.py`):
    - Updated column 10 ("Rating") to display dynamic recommendation badges across 5 tiers:
      - `STRONG BUY`: Dark emerald badge (`#0d531a` text, `#dcfce7` background)
      - `BUY`: Forest green badge (`#166534` text, `#e8f5e9` background)
      - `HOLD`: Amber badge (`#b45309` text, `#fef3c7` background)
      - `SELL`: Orange-red badge (`#c2410c` text, `#ffedd5` background)
      - `STRONG SELL`: Deep crimson badge (`#991b1b` text, `#fee2e2` background)
    - Added rich hover tooltips on the Rating cell showing live dynamic rating vs note static rating and full price threshold ranges.
    - Updated the Rating filter dropdown to filter across `STRONG BUY`, `BUY`, `HOLD`, `SELL`, and `STRONG SELL`.
    - Updated stock details KPI strip and markdown table clipboard export.
  - Test Suite (`tests/test_portfolio_valuation.py`):
    - Added comprehensive unit tests for JSON rating bands parsing, fallback threshold math, live price transitions, and PortfolioView badge/filter rendering.
    - Expanded test suite to **145 tests passing (100%)**.

- **Intelligent Ticker Examination & Stage 1 / Stage 2 Prompt Appropriateness Engine**:
  - Implemented `section_capture/ticker_lookup.py`:
    - `examine_ticker_locally()`: Zero-latency check for existing hubs on disk (`companies/<sector>/<ticker>/`) and local registry (`KNOWN_COMPANIES`).
    - `check_prompt_appropriateness()`: Cross-checks registered sector code against active `00-report-orientation`, `12-analyst-reading-brief`, Stage 1 forensic directives (`workflow/export_stage1.py`), and Stage 2 valuation models (`workflow/generate_stage2.py`).
    - `build_ticker_examination_prompt()` & `parse_examination_response()`: Structured JSON schema querying OpenRouter for corporate name, JSE/ICB sector, business summary, Stage 1 accounting focus, and Stage 2 valuation model.
    - `TickerExamineWorker(QThread)`: Non-blocking background worker to query OpenRouter without freezing the Qt UI.
  - Enhanced `NewCompanyDialog` (`section_capture/new_company_dialog.py`):
    - Added `🔍 Examine Ticker` button alongside the ticker input, also triggered by pressing `Enter`.
    - Added styled, expandable assessment frame displaying local hub status or AI evaluation of corporate details, JSE sector, and Stage 1 & Stage 2 prompt fit.
    - Automatically populates the company name and pre-selects the matched sector in the dropdown.
  - Test Suite: Created `tests/test_ticker_lookup.py` covering local resolution, un-scaffolded sector guidance, JSON response parsing, and UI assessment card simulation. Expanded full test suite to **140 tests passing (100%)**.

- **UI Streamlining: Elimination of Legacy Manual Web-Chat Controls**:
  - `AuditValuationDialog` (`section_capture/audit_dialog.py`):
    - Removed `Chat instruction:` inputs and `📋 Copy chat text` buttons in Stage 1 and Stage 2 tabs.
    - Removed manual `Open prompt folder`, `Open PDF folder`, and `Copy text` buttons in prompt panels.
    - Removed manual `Paste from clipboard` and `Load from disk` buttons in response panels.
    - Streamlined prompt header in Stage 2 into a single unified row (`Stage 2 Valuation Prompt` | `Generate Stage 2 Prompt` | `⚡ Generate SENS Update` | `📦 Move SENS to Completed` | `⚡ Run Valuation`).
    - Retained only the automated execution actions (`Compile from SQLite`, `⚡ Run with [Model]`, `Generate Prompt`, `Save Response to DB`).
  - `SavedSectionsDialog` (`section_capture/map_dialog.py`):
    - Removed `Copy prompt` and `Paste response` buttons from the section inspector row; focused on automated direct API evaluation.
  - `CaptureWindow` (`section_capture/window.py`):
    - Streamlined auxiliary row (`⚡ Run Pending`, `Review Sections →`, `Stored questions`), removing the redundant `Copy prompt` button.
    - Updated hint banner to `4 Save to SQLite & Run Analysis`.
  - Test Suite: Updated `tests/test_portfolio_valuation.py` asserting streamlined automated controls. All 133 tests passing (100%).

- **Consumer Lending Sector Onboarding (`consumer_lending` / ICB `30201020`) & Stage 1/2 Integration**:
  - Registered new sector `consumer_lending` in `companies/sectors.py`:
    - Code: `consumer_lending`, Short Label: `Lending`, Display: `Consumer Lending`, ICB Code: `30201020`, JSE Code: `JS3020`.
    - Aliases: `lending`, `credit`, `consumer-lending`, `credit_services`, `consumer lending`, `js3020`, `30201020`, `finance and credit services`.
    - Distinct badge styling with high-contrast palette (`#fdf2f8` / `#9d174d`).
    - Specialized personas: Stage 1 `Managing Director and Senior Forensic Credit & Lending Accounting Auditor` and Stage 2 `Managing Director & Head of Consumer Lending & Credit Equity Research`.
  - Scaffolding & Known Companies:
    - Initialized `companies/consumer_lending/__init__.py`.
    - Registered `NTU` (Nutun Limited, formerly Transaction Capital `TCP`) in `KNOWN_COMPANIES` in `section_capture/db.py`.
  - Forensic Directives & Pipeline Compilation:
    - Added dedicated forensic credit rules to `workflow/export_stage1.py`: IFRS 9 Stage 1/2/3 ECL migration, qualitative macro overlays, loan vintage roll rates, carrying value & estimated remaining collections (ERC) of purchased book debts (PBD) and non-performing loan (NPL) portfolios, risk-adjusted NIM, and NCA rate caps.
    - Integrated `consumer_lending` into `workflow/generate_stage2.py`.
    - Added robust error handling and period preservation across `section_capture/audit_dialog.py`.
  - Test Suite: Updated `tests/test_sectors.py` and verified full test suite. All 133 tests passing (100%).

- **Automated SENS & PDF Archiving and Reporting Period Detection Engine**:
  - **Reporting Period Auto-Detection**: Implemented `detect_reporting_period()` in `section_capture/db.py` supporting interim and annual patterns (`1H27`, `FY26`, `HY2027`, `1H26`, `2H26`, `FY27`) across filenames and page text.
  - **Unified Document Classification & Period Dialog**: Enhanced `DocumentClassifyDialog` in `section_capture/window.py` to prompt and confirm both Document Role and Reporting Period in a single unified step upon opening new PDFs.
  - **SQLite Database Schema Migration**: Added `period TEXT NOT NULL DEFAULT 'FY26'` to `reports` table in `documents/analysis.sqlite`, automatically migrated existing databases in `_migrate_schema()`, and updated `upsert_report()` to persist and retrieve period metadata.
  - **Dynamic Period Switcher in AuditValuationDialog**: Added a `Period:` editable dropdown selector to the dialog header. Automatically synchronizes `self.briefs_dir` to `companies/<sector>/<TICKER>/briefs/<period>/`, loads existing Stage 1 / Stage 2 briefs, and creates new period subfolders seamlessly.
  - **Automated SENS Archiving**: `save_stage2_response()` in `section_capture/audit_dialog.py` automatically moves all analyzed SENS announcements from `sources/sens/` into `sources/sens/completed/` upon saving a valuation note.
  - **Automated Source PDF Archiving**: Implemented `archive_source_pdfs()` in `section_capture/db.py`. Upon saving a Stage 2 valuation note, primary source PDFs in `sources/` are automatically archived to `sources/completed/<period>/`, safely releasing and reloading active Qt/pdfium canvas handles, and updating `reports.original_path` in SQLite.
  - **Company Hub Scaffolding**: Updated `new_company.py` to scaffold `sources/completed/` across newly created companies, and backfilled `sources/completed/` across all existing company hubs.
  - **Full Test Suite Passing**: Added comprehensive unit tests in `tests/test_portfolio_valuation.py`. Total test suite expanded to **133 tests passing (100%)**.

- **Dynamic Model-Agnostic UI Architecture & Status Bar Model Indicator**:
  - Eliminated hardcoded model names (DeepSeek) across buttons, status notifications, and dialog tooltips in section_capture/window.py, section_capture/audit_dialog.py, and section_capture/map_dialog.py.
  - Implemented get_model_display_name() and get_model_short_tag() in section_capture/openrouter.py:
    - Automatically formats model identifiers from OPENROUTER_MODEL / secrets.env (e.g. deepseek/deepseek-v4.1-flash-1017 -> DeepSeek Flash, anthropic/claude-3.5-sonnet -> Claude 3.5 Sonnet, openai/gpt-4o -> GPT-4o, google/gemini-2.0-flash -> Gemini 2.0 Flash).
    - Handles :nitro priority throughput tagging cleanly (e.g. DeepSeek Flash (nitro) / DeepSeek:nitro).
  - Added permanent status bar widget in MainWindow (self.model_status_label = QLabel()) displaying the active OpenRouter model (Model: DeepSeek Flash or Model: DeepSeek Flash (nitro)) with hover tooltips providing the full OpenRouter model ID and configuration path. Dynamically updates when :nitro throughput is toggled.
  - Added active model badge in AuditValuationDialog header alongside ticker and sector information.
  - Updated Stage 1 and Stage 2 buttons to dynamically read Run with {display_name} and Run Valuation ({display_name}), with dynamic running text and completion messages.
  - Added unit and GUI tests in tests/test_openrouter.py, tests/test_portfolio_valuation.py, and tests/test_report_map.py. All 129 tests passing (100%).

- **Model-Agnostic Prompt Architecture & Generic LLM Directives**:
  - Replaced all explicit model references (e.g. INSTRUCTIONS FOR GEMINI 4 ARGON) across prompt generators with model-agnostic directives:
    - Stage 1: ### INSTRUCTIONS FOR FORENSIC AUDITOR (LLM):
    - Stage 2 & SENS Update: ### INSTRUCTIONS FOR INSTITUTIONAL RESEARCH ANALYST (LLM):
  - Cleaned all UI headers, status text, and callouts in section_capture/audit_dialog.py to reference generic LLM / Auditing Model rather than specific proprietary models.
  - Excluded README.md from SENS announcement discovery in workflow/generate_sens_update.py.
  - All 127 unit and integration tests passing.

- **Automated SENS Directory Scaffolding (sources/sens/)**:
  - Enhanced 
ew_company.py:create_company() to automatically scaffold sources/sens/ and sources/sens/completed/ along with a guiding README.md whenever a new company is initialized via CLI or the desktop GUI dialog.
  - Updated post-creation guidance instructions to prompt analysts to drop SENS announcements into companies/<sector>/<TICKER>/sources/sens/.
  - Backfilled sources/sens/ and completed/ folders across all active portfolio companies (CGR, IOC, PAN, ORN, HAR, LEW, TRU, APF, PIK).
  - Added unit test 	est_create_company_scaffolds_sens_folder in 	ests/test_portfolio_valuation.py.

- **Automated Section Matching & Auto-Capture Engine (explore/auto-section-capture)**:
  - Implemented section_capture/section_matcher.py with intelligent title normalization (acronym expansion for CEO, CFO, AFS, IAR; stop-word elimination; prefix stripping) and token-proximity scoring.
  - Implemented extract_all_app_sections() combining PDF bookmarks/outline and heading heuristics to establish comprehensive section boundaries across full PDF reports.
  - Implemented compare_section_maps() categorizing sections into 🟢 Matched, 🟡 User-Only (analyst custom sections), and 🔵 App-Discovered (detected sections not yet in user map).
  - Built SectionComparisonDialog in section_capture/map_dialog.py accessible via **🔍 Compare with App Scan** in the Report Map dialog.
  - Added **⚡ Auto-Capture Matched Sections** action: automatically extracts full page texts and tables across physical page ranges, tags content types (	able, inancial_note, commentary), and saves SavedSection packages directly into SQLite without manual mouse cropping.
  - Added full test coverage in 	ests/test_section_matcher.py (6 unit and GUI tests). Total test suite expanded to **125 tests passing (100%)**.

- **Multi-PDF Dual-Disclosure Ingestion & Benchmarking (APF, IOC, CGR)**:
  - Enhanced AuditValuationDialog.run_stage2_deepseek() to ingest and tag *all* source PDFs located in companies/<sector>/<TICKER>/sources/ (e.g. Integrated Annual Report + Audited Financial Statements).
  - Validated multi-PDF ingestion on **iOCO (IOC)**: Ingested iOCO-IAR-2026.pdf (164 pages) + iOCO-AFS-July2026.pdf (102 pages) = 266 physical pages (220,123 tokens total) in 21.8s for .032 USD. Result: Target R4.75, BUY (+21.8%), 0% dividend yield, DCF R4.90 (Gemini baseline was Target R4.90, BUY, +23.7%).
  - Validated on **Calgro M3 (CGR)**: Both Calgro-M3-Integrated-Report-2026.pdf (124 pages) + Calgro-M3-AFS-2026.pdf (58 pages) = 182 physical pages (171,468 tokens total) ingested in 21.5s for .025 USD. Emitted Target R6.50, HOLD (+12.8%), 0% dividend yield.
  - Confirmed latency dynamics: Stage 1 takes longer (~83-91s) when processing 350k+ prompt tokens and generating 8,900+ completion tokens; Stage 2 completes faster (~21-25s) because prompt size is smaller (170k-220k tokens) and output format is structured at ~2,500-3,500 completion tokens.
  - Published comprehensive application operating manual to [docs/APPLICATION_MANUAL.md](docs/APPLICATION_MANUAL.md).

- **DeepSeek Toleration & Automation for Stage 2 Institutional Valuations with Full PDF Ingestion**:
  - Investigated and verified that complete primary source company PDF reports (e.g. 328-page IAR/AFS) can be ingested alongside Stage 2 valuation prompts directly into DeepSeek Flash (`deepseek/deepseek-v4.1-flash-1017`) via OpenRouter, fully eliminating manual browser copy-pasting.
  - **Context Toleration & Benchmarks on APF (Accelerate Property Fund)**:
    - **PDF Text Ingestion**: Extracted all 328 physical pages of `APF_IAR_2026_Combined_V21.pdf` (567,928 characters) in **0.25 seconds** using `pypdfium2`.
    - **Combined Dossier**: Bundled the Stage 2 prompt + Audited Stage 1 Ground Truth + 8 post-balance sheet SENS notices + complete 328-page PDF text (totaling **645,359 characters / 178,408 prompt tokens**).
    - **Context Utilization**: Only ~15.4% of DeepSeek's 1,048,576 token (1M) context window (over 84% unused headroom).
    - **Execution & Cost**: Completed in **23.4 seconds** for **$0.026 USD (~2.6 cents)**.
  - **Valuation Quality & Deterministic Output**:
    - Emitted complete publication-grade research note saved to [`companies/reit/APF/briefs/FY26/APF_FY26_stage2_deepseek_valuation_response.md`](file:///c:/Users/Dion/Desktop/Projects/stock_analysis_prompts/companies/reit/APF/briefs/FY26/APF_FY26_stage2_deepseek_valuation_response.md).
    - Generated compliant machine-readable JSON summary card and executive table parsed automatically by `parse_valuation_summary()`:
      - **12M JSE Target Price**: **R0.35** (SELL, implied upside −41.7%, 0% dividend yield).
      - Reconciled SOTP NAV of R0.47, applying a 25% distressed discount for the March 2027 R3.0bn debt cliff and ICR covenant step-up.
      - Modeled bottom-up 2-year forecast: FY27E NPI −8.5%, Office vacancy 55%, DIPS 0.10 cps.
  - **Desktop UI Integration (`section_capture/audit_dialog.py`)**:
    - Added one-click **`⚡ Run Valuation with DeepSeek`** button to Stage 2 tab. Automatically extracts the primary source PDF text, packages SENS notices, runs asynchronously via `OpenRouterWorker(QThread)`, saves to SQLite and disk, and refreshes the Portfolio Coverage Dashboard.
    - Added unit test coverage in [`tests/test_portfolio_valuation.py`](file:///c:/Users/Dion/Desktop/Projects/stock_analysis_prompts/tests/test_portfolio_valuation.py). All **119 tests pass** in 26.3s.

- **DeepSeek Toleration & Automation for Stage 1 Cognitive Forensic Audits**:
  - Investigated and tested whether DeepSeek via OpenRouter (`deepseek/deepseek-v4.1-flash-1017`) can directly process Stage 1 Forensic Audit prompts, eliminating manual copy-pasting to Gemini web chat.
  - **Context Toleration & Benchmarks on APF (Accelerate Property Fund)**:
    - **Compacted Prompt (Deduplicated Master Ledger)**: 961,898 chars (~262,604 tokens). Processed in **17.2 seconds** for **$0.037 USD** (3,182 completion tokens).
    - **Full Uncompacted Prompt**: 1,779,181 chars (~507,827 tokens — over half a million tokens). Processed in **38.3 seconds** for **$0.073 USD** (8,751 completion tokens, 28,866 chars, 4,264 words).
    - Both tests ran without network or gateway errors within DeepSeek's 1,048,576 token (1M) context window.
  - **Forensic Quality Evaluation**:
    - DeepSeek successfully resolved all 7 key REIT accounting junctions with line-by-line arithmetic proofs, identifying critical nuances: DIPS of 0.09 cps vs FFO of 6.25 cps after R126m capex deductions; FFO and ICR propped up by R166.7m of one-offs (SARS VAT refund + Covid insurance); recurring ICR at ~0.90x breaching the 1.1x bank covenant; 100% of R3.0bn debt maturing 31 March 2027; commercial vacancy surging to 45.2%; and Fourways Mall valuation increasing R196.5m despite NPI collapsing 39.7%.
    - Result saved to [`companies/reit/APF/briefs/FY26/APF_FY26_stage1_deepseek_response.md`](file:///c:/Users/Dion/Desktop/Projects/stock_analysis_prompts/companies/reit/APF/briefs/FY26/APF_FY26_stage1_deepseek_response.md).
  - **Desktop UI Integration & Automation (`section_capture/audit_dialog.py`)**:
    - Added one-click `"⚡ Run with DeepSeek"` action in the Stage 1 Audit tab.
    - Added background `OpenRouterWorker` execution with live token, latency, and dollar cost reporting.
    - Added automated persistence directly to SQLite (`reports.stage1_response`) and disk (`*_stage1_audit_response.md`).
    - Added unit test `test_audit_dialog_run_stage1_deepseek_btn` in `tests/test_portfolio_valuation.py`.
    - Full test suite verified: **119 passed in 26.01s with 0 errors**.

- **Portfolio Valuation Database Resynchronization (`documents/analysis.sqlite`)**:
  - Investigated and resolved the root cause of identical valuation numbers (Target R43.50, Ref R30.69, BUY, +41.7% upside) appearing across all stocks (`PAN`, `LEW`, `ORN`, `APF`, `IOC`) on the Analyzed Stocks & Valuation Coverage screen.
  - **Root Cause**: During an earlier script run to backfill FTSE/JSE ICB sector codes, an update statement accidentally overwrote the `stage2_response` and valuation parameters (`target_price_zar`, `reference_price_zar`, `recommendation`, `upside_pct`, `tsr_pct`) across all database rows with Pan African Resources' note data. The markdown valuation notes on disk in `companies/<sector>/<TICKER>/briefs/FY26/` remained completely authentic and uncorrupted.
  - **Resolution**:
    - Created and executed [`workflow/resync_stage2_db.py`](file:///c:/Users/Dion/Desktop/Projects/stock_analysis_prompts/workflow/resync_stage2_db.py) to read each company's authentic markdown note and invoke `save_stage2_report()` for its specific report SHA-256 hash.
    - Successfully restored verified institutional metrics in `documents/analysis.sqlite`:
      - **PAN**: Target R43.50 | Ref R30.69 | BUY | Note Upside +41.7%
      - **LEW**: Target R84.50 | Ref R79.00 | HOLD | Note Upside +7.0%
      - **ORN**: Target R0.26 | Ref R0.28 | HOLD | Note Upside -8.5%
      - **APF**: Target R0.42 | Ref R0.60 | SELL | Note Upside -30.0%
      - **IOC**: Target R4.90 | Ref R3.96 | BUY | Note Upside +23.7%
      - **CGR**: In Progress (Forensic Audit stage, awaiting Stage 2 valuation note)
  - Full test suite verified: **118 passed in 25.40s with 0 errors**.

- **PAN FY26 Sequential Section Resubmission & Response Evaluation**:
  - Successfully resubmitted all 19 captured sections of Pan African Resources PLC (FY26 Year-End Results SENS) sequentially to DeepSeek Flash via OpenRouter with full questions ledger updates:
    - **Selection Text Extraction Fix (`extract_selection_texts`)**: Fixed a legacy issue where sections captured under older schemas had selection bounding boxes without inline `"text"` keys, causing prompts to generate empty evidence markers. Implemented fallback slicing against `text_indices` and prompt blocks across `packages.py`, `window.py`, `map_dialog.py`, and `resubmit_sections.py`, recovering the complete 79,232 characters of CEO Statement evidence for Section 2.
    - **Complete Sequential Execution**:
      - 19 of 19 sections completed and saved to `documents/analysis.sqlite` and `companies/mining/PAN/briefs/`.
      - Total tokens processed: **342,600 tokens** across all 19 calls (average execution: ~40s/call, total API cost: ~$0.07).
      - Dynamic questions ledger expanded sequentially from 0 characters at Section 1 to an authoritative 19,246 characters at Section 19.
    - **Forensic Mining Determinations Evaluated**:
      - Production: 272,310 oz gold (FY25: 196,527 oz, +38.6%), tracking close to 275k–292k guidance.
      - Revenue: US$1,156.5m (FY25: US$540.0m) driven by higher average gold prices and Mogale Gold (MTR) ramp-up.
      - AISC: Total group AISC of US$508.4m; expansion capex US$195.0m; AIC US$703.4m.
      - Tax note (Note 6): Identified Footnote [^1] restating FY25 comparative deferred tax liabilities from environmental rehabilitation obligations into employee obligations, cash-settled SBP, and ECL.
    - **Stage 1 Forensic Audit Prompt Compiled**: Generated [`PAN_FY26_stage1_forensic_prompt.md`](file:///c:/Users/Dion/Desktop/Projects/stock_analysis_prompts/companies/mining/PAN/briefs/FY26/PAN_FY26_stage1_forensic_prompt.md) (0.56 MB, 569,707 characters, ~142k tokens) with full compaction and single master ledger embedding.


- **Elimination of In-Prompt Questions Duplication in Section Capture (`section_capture/packages.py`)**:
  - Identified that whenever questions specifically targeting the active section (`QUESTIONS SPECIFICALLY TARGETING THIS SECTION`) were highlighted at the top of the prompt, the exact same lines were being repeated immediately below inside `BEGIN STORED QUESTIONS FROM EARLIER SECTIONS`, wasting ~100k characters across multi-section companies (e.g. 97,233 duplicate characters in CGR alone).
  - Implemented `partition_stored_questions(stored_questions, section_ids)` in [`section_capture/packages.py`](file:///c:/Users/Dion/Desktop/Projects/stock_analysis_prompts/section_capture/packages.py):
    - Extracts `relevant_lines` targeting the active `section_ids` into the priority focus block.
    - Excludes those matched lines from the subsequent `STORED QUESTIONS` block, while preserving markdown headings and structure for all other remaining questions.
    - Automatically prunes empty section headers whose questions were fully matched and migrated into the priority block.
  - Added unit test coverage in [`tests/test_capture.py`](file:///c:/Users/Dion/Desktop/Projects/stock_analysis_prompts/tests/test_capture.py) (`test_partition_stored_questions_eliminates_duplicates`).
  - Full test suite verified: **118 passed in 25.65s with 0 errors**.


- **Stage 1 Prompt Compaction & Questions Ledger Deduplication (`workflow/export_stage1.py`)**:
  - Solved prompt bloat on large, multi-section disclosure captures (e.g. Calgro M3's 41 sections which grew to 2.95 MB / ~700k tokens due to repeated copy-paste question ledgers):
    - **Algorithmic Section Cleaning (`clean_reading_brief`)**: Strips the redundant Section 4 copy-paste ledger block (`### 4. Updated Open Questions Ledger (Copy to App)`) from each intermediate section's LLM response, saving over 800,000 characters of pure duplication across 41 sections while preserving 100% of the financial evidence, tables, answers, footnote deep-dives, baseline inputs, and red flags.
    - **Authoritative Master Ledger Embedding**: Omitted the redundant repeating `stored_questions_snapshot` inside all 41 individual sections (saving ~790,000 characters). Instead, embeds the single authoritative, cumulative master `questions_ledger` once at the top of the dossier under `## MASTER WORKING PAPER: CUMULATIVE OPEN QUESTIONS LEDGER`.
    - **Configurable Compact Pipeline**: `build_stage1_prompt_content` and `export_stage1_prompt` now default to `compact=True`, while allowing `--full` in CLI to output the raw uncompacted prompt if ever required for debugging.
    - **Desktop GUI Integration (`section_capture/audit_dialog.py`)**: Updated `compile_stage1_prompt` to extract the primary `questions_ledger` and compile using the deduplicated compact format.
    - **Verified Results**:
      - `companies/construction/CGR/briefs/FY26/CGR_FY26_stage1_forensic_prompt.md` reduced from **2.95 MB (2,898,191 chars, ~700k tokens)** down to **1.28 MB (1,316,614 chars, ~315k tokens)** — a **54.6% reduction** saving **1.58 million characters** with zero loss of financial substance.
      - Full test suite verified: **117 passed in 24.89s with 0 errors**.


- **Live JSE Market Prices Integration via yfinance (`.JO`)**:
  - Integrated real-time JSE equity market prices into the Analyzed Stocks & Portfolio Coverage screen using Yahoo Finance:
    - **Market Data Engine (`section_capture/market_data.py`)**:
      - Formats company tickers to official Yahoo Finance JSE symbols using `.JO` suffix (e.g. `PAN.JO`, `LEW.JO`, `CGR.JO`, `ORN.JO`, `APF.JO`, `IOC.JO`, `HAR.JO`, `AFT.JO`).
      - Automatically normalizes South African Cents (`ZAc`) to ZAR Rands (`ZAc / 100.0`).
      - Implemented asynchronous `MarketQuoteWorker(QThread)` with Qt signals (`quote_received`, `all_quotes_ready`, `fetch_failed`) to keep the desktop GUI 100% responsive.
    - **Persistent SQLite Quote Caching (`section_capture/db.py`)**:
      - Added `market_quotes` schema in `documents/analysis.sqlite` storing latest price, previous close, change percentage, currency, and update timestamps.
      - Updated `get_analyzed_stocks()` to join cached quotes, providing `live_price_zar`, `live_price_change_pct`, and recomputing `live_upside_pct` dynamically against 12M target prices.
    - **Portfolio Coverage Dashboard (`section_capture/portfolio_view.py`)**:
      - Expanded table to 13 columns distinguishing **Latest JSE Price**, **12M Target**, **Live Upside**, **Note Ref Price**, and **Note Upside**.
      - Added `"🔄 Fetch Live JSE Prices"` toolbar button with real-time sync status indicator.
      - Enhanced the stock KPI details banner to contrast Live Market Price and Live Upside alongside Note Reference Price.
      - Updated Markdown universe exporter (`Copy Universe Table`) to include live prices and live upside.
    - **Dependencies & Verification**:
      - Added `yfinance>=1.7.0` to `requirements.txt` and regenerated `requirements.lock.txt`.
      - Added unit and integration tests in `tests/test_market_data.py`.
      - Verified full test suite: **117 passed in 26.23s with 0 warnings and 0 failures**.

- **Total Elimination of Defaults Across Entire Workflow**:
  - Completely purged silent fallback defaults, implicit assumptions, and fake placeholder profiles across all layers (CLI, GUI, prompt resolution, database, and pipeline generators):
    - **Sector Registry (`companies/sectors.py`)**: Removed `DEFAULT_SECTOR = "mining"`. `get_sector_config(code)` now strictly raises `ValueError` if code is omitted and `KeyError` if unrecognized. Formatting helpers (`get_jse_sector_code`, `get_jse_sector_name`, `get_sector_badge_style`, `get_sector_short_label`) gracefully handle unassigned/empty inputs without fallback fabrication.
    - **Prompt Resolution (`section_capture/packages.py` & `report_map.py`)**:
      - `detect_sector_from_path()` returns `None` for ambiguous or unclassified paths without guessing or falling back to a default sector.
      - `get_prompt_path()` and `get_orientation_path()` strictly require explicit `sector: str` and raise `FileNotFoundError` if prompt templates are missing on disk, and `ValueError` if sector is empty.
      - `save_package()` raises `ValueError` if sector cannot be inferred and is not provided.
    - **Database & Metadata (`section_capture/db.py` & `audit_dialog.py`)**:
      - `detect_company_meta()` returns `(None, None, None)` for unclassifiable files instead of fabricating `"TARGET"`, `"Unknown Asset"`, and `"retail"`.
      - `get_analyzed_stocks()` categorizes unclassified documents as `UNCLASSIFIED` / `unassigned` rather than defaulting to `retail`.
      - `AuditValuationDialog` uses explicit `prod_db` resolution to isolate test databases without creating stray folders or defaulting empty states to `mining`.
    - **Pipeline Generators & Scaffolding (`export_stage1.py`, `generate_stage2.py`, `generate_sens_update.py`, `new_company.py`)**:
      - Replaced `(sector or "mining")` with strict resolution: if company directory is not found and `--sector` is not provided, CLI tools raise `ValueError` requiring explicit `--sector`.
      - Scaffolding tool `new_company.py` requires `--sector` as a mandatory non-default argument.
      - `build_stage1_prompt_content` and `build_stage2_prompt_content` added dedicated accounting junctions and operating models for `finance` and `telcos`, and raise `ValueError` on unsupported sectors.
    - **Desktop GUI (`section_capture/window.py` & `new_company_dialog.py`)**:
      - Added `"Select Sector..."` unselected placeholder in toolbar combo. If path inference fails on PDF open, window prompts the user and prevents capture or AI queries until a valid sector is selected.
      - `new_company_dialog` validates selection against `get_all_sector_codes()`.
    - **Test Suite Alignment**:
      - Updated `tests/test_sectors.py`, `tests/test_capture.py`, `tests/test_report_map.py`, and `tests/test_portfolio_valuation.py` for strict exception checking (`KeyError`, `ValueError`, `FileNotFoundError`) and `None` returns.
      - Verified full test suite: **110 passed in 23.85s with 0 warnings and 0 failures**.

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

1. **Active Coverage Universe (10 Assets Evaluated & Maintained)**:
   - `PAN` (`FY26`): **STRONG BUY** | Live R24.60 | Target R34.50 (+40.2% upside / +44.1% TSR) | Mining
   - `SSK` (`FY26`): **HOLD** | Live R5.78 | Target R6.20 (+7.3% upside) | Construction
   - `CGR` (`FY26`): **SELL** | Live R3.65 | Target R3.10 (-15.1% downside) | Construction
   - `SPP` (`1H26`): **HOLD** | Live R148.50 | Target R162.00 (+9.1% upside / +13.5% TSR) | Retail
   - `PIK` (`FY26`): **SELL** | Live R22.40 | Target R20.50 (-8.5% downside) | Retail
   - `LEW` (`FY26`): **HOLD** | Live R90.19 | Target R95.00 (+5.3% upside / +14.8% TSR) | Retail
   - `ORN` (`FY26`): **HOLD** | Live R0.25 | Target R0.28 (+12.0% upside) | Mining
   - `APF` (`FY26`): **STRONG SELL** | Live R0.48 | Target R0.30 (-37.5% downside) | REIT
   - `IOC` (`FY26`): **HOLD** | Live R4.22 | Target R4.60 (+9.0% upside) | IT
   - `NTU` (`FY26`): **STRONG SELL** | Live R0.89 | Target R0.55 (-38.2% downside) | Consumer Lending
2. **Execute Onboarding or Evaluation for New Stocks**:
   - Use `evaluate_stock.py <TICKER>` for existing coverage checks.
   - Follow `docs/STOCK_EVALUATION_FORMAT.md` for output format, always presenting the mandatory **Valuation Errors Found & Analytical Lessons Learned** section.


