# Independent Review Report — Agentic Report Build P4 (PAN FY26)

**Target Commit**: [`636be8a`](file:///C:/Users/diond/Desktop/Projects/stock_prompts_agentic/workflow/changes/20261029_agentic_report_build/) on branch `agentic-report-build`  
**Review Standard**: Independent evaluation per [`reviews/p4_review_pack/PROMPT.md`](file:///C:/Users/diond/Desktop/Projects/stock_prompts_agentic/reviews/p4_review_pack/PROMPT.md)  
**Evaluator**: Gemini-role pass (Antigravity) + Codex-role evidence verification against the source PDF  
**Source PDF**: [`companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf`](file:///C:/Users/diond/Desktop/Projects/stock_prompts_agentic/companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf) (SHA-256 `62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd`, 54 physical pages)  
**Database**: [`workflow/changes/20261029_agentic_report_build/build/report.sqlite`](file:///C:/Users/diond/Desktop/Projects/stock_prompts_agentic/workflow/changes/20261029_agentic_report_build/build/report.sqlite) (4,800 cells, 97 conflicts, 8 ledger questions)  
**Suite Status**: 109/109 passed in 0.24s across 11 test modules.

---

## Executive Summary

The agentic report build represents a disciplined, deterministic extraction and reconciliation effort: **zero printed figures were overwritten**, and arithmetic relationships executed in [`tests_reconcile/`](file:///C:/Users/diond/Desktop/Projects/stock_prompts_agentic/workflow/changes/20261029_agentic_report_build/tests_reconcile/) run strictly in code.

However, an independent adversarial review reveals four key areas where **the brief's confidence exceeds its evidence**, tables in the PDF were dropped, and figures were asserted without suite verification:

1. **Major Omitted Table**: Note 18 (Acquisition of Emmerson Resources Limited, p.34) was discarded by the extractor due to a modal-width filter mistaking a US\$160.1m acquisition consideration and net asset allocation table for "caption fragments". Its US\$142.4m addition to Property, Plant & Equipment (Note 7) was never verified.
2. **Untested Assertions in the Brief**: Multiple headline figures in [`READING_BRIEF_CONSOLIDATED.md`](file:///C:/Users/diond/Desktop/Projects/stock_prompts_agentic/workflow/changes/20261029_agentic_report_build/READING_BRIEF_CONSOLIDATED.md)—including Basic & Diluted EPS (17.60 / 7.16 cents), Total Comprehensive Income (US\$400,965k / US\$155,554k), Levered Free Cash Flow (US\$201.8m), Net Cash (US\$(185.7)m), and individual segment revenues—are asserted without corresponding test assertions in [`tests_reconcile/`](file:///C:/Users/diond/Desktop/Projects/stock_prompts_agentic/workflow/changes/20261029_agentic_report_build/tests_reconcile/). The claim that the cascade rolls to "total comprehensive income" is unexecuted.
3. **Premature Ledger Closures in Prose**: The brief declared `Q-e8c872e6edc94d18` "Resolved" and `Q-a0b503d7ac044eee` "Substantially resolved" based purely on arithmetic ties, despite underlying definitional and accounting intent remaining unaddressed. In contrast, the SQLite database properly kept both questions `open`.
4. **Lineage Inconsistencies**: The `document` column in `cells` is heterogeneous (1,196 cells carry a local Windows file path, 3,604 carry the document SHA-256), and `extraction_commit` stores human build phase strings (`p1_extraction_v3`) rather than git commit hashes. Note 17 (p.34) is claimed as "covered" in the header of the brief but simultaneously listed as "unverified" with zero tests.

---

## 1. Gemini-Role Pass: Adherence and Self-Consistency

### 1.1 Covenant 1 — Never replace a printed figure
- **Finding**: **PASSED (Strict Adherence)**.
- **Verification**:
  - Barberton FY26 Total Operations: Stored verbatim in `cells` as `94,929` (physical page 49, col 9). It was not replaced with `84,929`. The 10,000 oz discrepancy is evaluated strictly as a conditional hypothesis (`test_fy26_barberton_components_exceed_by_10000`) and logged in `conflicts` (`M3|p49|...`) and ledger `Q-1f48aa6d4b884f09`.
  - Elikhulu FY25 ZAR all-in cost: Stored verbatim as `68,843` (p.49, col 5) with implied order-of-magnitude conflict logged (`XR_ALLIN|p49|...`) and open question `Q-f1a4ce3647724ed9`.
  - MTR FY25 tailings: Stored verbatim as `25,043` (p.48, col 6) against total `30,806` (col 11) with conflict logged (`M2|p48|...`) and open question `Q-3e8730dbd1994205`.
  - Adjusted EBITDA: Both published scopes (US\$663.1m operating on p.50 vs US\$609,431k group on p.22) and the p.45/p.50 Barberton variance (142.5 vs 142.4) are preserved verbatim in SQLite.

### 1.2 Covenant 2 — Arithmetic in code
- **Finding**: **PARTIAL (Gaps between Brief Assertions and Suite Execution)**.
- While the suite executes 109 tests covering primary identities and segment sums, several figures stated as facts in the brief are **asserted without test verification**:
  1. *Basic and Diluted EPS*: The brief asserts `17.60 US cents (FY26) / 7.16 US cents (FY25)`. These cells exist in SQLite (p.18, p.4), but appear 0 times in [`tests_reconcile/`](file:///C:/Users/diond/Desktop/Projects/stock_prompts_agentic/workflow/changes/20261029_agentic_report_build/tests_reconcile/).
  2. *Total Comprehensive Income*: Brief Section 2, item 2 claims: *"Income statement cascade holds: revenue to gross profit to operating profit to profit before tax to net profit, and to total comprehensive income."* In [`test_primary_statements.py`](file:///C:/Users/diond/Desktop/Projects/stock_prompts_agentic/workflow/changes/20261029_agentic_report_build/tests_reconcile/test_primary_statements.py), the cascade check stops at profit for the period. The word `comprehensive` appears nowhere in `tests_reconcile/`.
  3. *Unasserted Final Totals*: In [`test_apm_ratios.py`](file:///C:/Users/diond/Desktop/Projects/stock_prompts_agentic/workflow/changes/20261029_agentic_report_build/tests_reconcile/test_apm_ratios.py) and [`test_apm_capital.py`](file:///C:/Users/diond/Desktop/Projects/stock_prompts_agentic/workflow/changes/20261029_agentic_report_build/tests_reconcile/test_apm_capital.py), tests verify component sums (`built == printed`), but never assert the actual printed totals: Levered Free Cash Flow (US\$201.8m), Net Cash (US\$(185.7)m), or Net Senior Cash (US\$(194.7)m).
  4. *Segment Revenue Disaggregation*: Individual segment revenues (Barberton 352,807, Evander 441,978, MTR 228,268, Tennant 132,804, Agricultural ESG 594) are verified only as column sums (`sum(cols 0..4) == col 5`), without checking the individual numbers against constants.

### 1.3 Covenant 3 — Lineage
- **Finding**: **ACCEPTABLE WITH IDENTIFIED SCHEMA DEFECTS**.
- **Page coverage**: 100% of the 4,800 cells carry valid physical pages (1..54).
- **Document hash defect**: The `document` column in `cells` is split:
  - 1,196 cells (D009 extraction) contain the local machine absolute path: `C:\Users\diond\Desktop\Projects\stock_prompts_agentic\companies\mining\PAN\sources\Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf`.
  - 3,604 cells contain the SHA-256 hash `62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd`.
  - The document SHA-256 is correctly recorded in the `sources` table.
- **Extraction commit defect**: `extraction_commit` contains build pipeline identifiers (`p1_extraction_v3`, `p1_primary_statements_v1`, `p1_note3_segments_v2`), not 7-character or 40-character Git commit SHAs.
- **Unverified pages labelling**:
  - The brief lists 13 pages as `[printed, unverified]`: `pp.4, 6, 9, 10, 19, 26, 29, 30, 31, 34, 35, 36, 39`.
  - *Conflict*: The brief's header lists Note 17 (p.34) as a *covered section* (`Notes 4, 7, 16, 17 (pp.25, 27-28, 32-34)`), yet p.34 has zero test assertions in `tests_reconcile/` and is listed in the body as unverified.

### 1.4 Covenant 4 — Ledger independence
- **Finding**: **HELD IN DATABASE, VIOLATED IN BRIEF PROSE**.
- In [`build/report.sqlite`](file:///C:/Users/diond/Desktop/Projects/stock_prompts_agentic/workflow/changes/20261029_agentic_report_build/build/report.sqlite), all 8 questions maintain `status = 'open'`.
- In [`READING_BRIEF_CONSOLIDATED.md`](file:///C:/Users/diond/Desktop/Projects/stock_prompts_agentic/workflow/changes/20261029_agentic_report_build/READING_BRIEF_CONSOLIDATED.md) Section 5:
  - `Q-e8c872e6edc94d18` is prematurely labelled **Resolved** because `26,748 + 1,081 = 27,829`. The underlying accounting intent (why buy-in gold was embedded into the underground column) was not answered.
  - `Q-a0b503d7ac044eee` is labelled **Substantially resolved** based on a revenue tie (`1,155,857 + 594 = 1,156,451`), which does not resolve the AISC/AIC cost definitions or ZAR translation basis raised in the question.

### 1.5 Honesty of the defect log
- **Finding**: **VERIFIED AS HONEST AND CONTEMPORANEOUS**.
- Inspection of the git log shows real, unvarnished revisions:
  - Commit `8dc69c6` (`APM p.44 attempted and reverted`): The geometry extractor failed because the left-hand capital table (6 cols) and right-hand debt tables (2 cols) share overlapping y-coordinates. The commit honestly reverted the DB to 2,436 cells and logged root causes in `WORKPLAN_APM.md`.
  - Commit `e041176`: Successfully rebuilt p.44 via `textpage.get_text_range()` stream order.
  - Commit `667f804` and `7528fd8`: Logged why p.28 initially failed—a modal-width filter discarded the 14-column balance and carrying-amount rows because a leading four-digit year token altered the token count. Removing the modal-width filter recovered all 16 rows / 224 cells.

---

## 2. Codex-Role Pass: Verification Against the Source PDF

### 2.1 Spot-check of printed figures on pp.48–50
Verified against PDF text layer and `cells` table:
1. `Tonnes milled – underground` for BTRP (p.48, col 3): Printed glyph is `–` (en-dash, `\u2013`). Database stores `value_raw = '–'`, `value_num = NULL`. Exact glyph match.
2. `Gold produced – total` Group total (p.49, col 13): Printed glyph is `272,310`. Database stores `value_raw = '272,310'`, `value_num = 272310.0`. Exact glyph match.
3. `Gold produced – total` Barberton total (p.49, col 9): Printed glyph is `94,929`. Database stores `value_raw = '94,929'`, `value_num = 94929.0`. Exact glyph match.
4. `Revenue` Group total (p.50, col 13): Printed glyph is `17,249.1`. Database stores `value_raw = '17,249.1'`, `value_num = 17249.1`. Exact glyph match.
5. `Capital expenditure US$` Group total (p.50, col 13): Printed glyph is `214.9`. Database stores `value_raw = '214.9'`, `value_num = 214.9`. Exact glyph match.

### 2.2 Balance sheet, income statement anchors & cash tie (pp.17–18)
- **Balance Sheet (p.17)**: Total assets = `1,608,075` (FY26) / `1,004,509` (FY25); Total equity & liabilities = `1,608,075` (FY26) / `1,004,509` (FY25). Ties to the dollar.
- **Income Statement (p.18)**: Revenue = `1,156,451` (FY26) / `540,033` (FY25); Profit for period = `356,911` (FY26) / `140,605` (FY25).
- **Cash Tie**: Cash & cash equivalents on Balance Sheet (p.17) is `108,312` (FY26) / `49,532` (FY25). On Cash Flow Statement (p.18), closing cash is `108,312` (FY26) / `49,532` (FY25). Exactly matches across both statements in the PDF and SQLite.

### 2.3 Segment analysis columns (pp.21–24)
- **Column sequence in PDF**:
  - `0`: Barberton Mines
  - `1`: Evander Mines
  - `2`: Solar projects
  - `3`: MTR operation
  - `4`: Tennant Mines
  - `5`: Mining operations (subtotal)
  - `6`: Exploration assets
  - `7`: Agricultural ESG projects
  - `8`: Corporate
  - `9`: Funding Company
  - `10`: Group total
- **Sums**: Mining operations subtotal (col 5) correctly sums cols 0..4 across all 72 rows. Group total (col 10) correctly sums col 5 + cols 6..9 across all 72 rows.
- **The US\$594k revenue line**: In the PDF on p.21, `594` is the only number between Mining operations (1,155,857) and Group total (1,156,451). Note 4 on p.25 breaks down revenue as Gold (1,148,460), Silver (4,792), Copper (2,605), and Blueberries (594). Blueberries represents Agricultural ESG projects, confirming the column assignment is physically and economically correct.

### 2.4 Adjusted EBITDA 142.5 vs 142.4 & ROCE inputs (pp.44–47)
- **Adjusted EBITDA**:
  - p.45 APM table: Barberton Mines Adjusted EBITDA prints `142.5`.
  - p.50 D009 table: Mining operations | Barberton Mines Adjusted EBITDA prints `142.4`.
  - Both figures exist in the PDF and are captured in SQLite. This 0.1 difference explains why the sum of printed leaves on p.50 is 663.0 while the printed group total is 663.1.
- **ROCE Inputs (p.47)**:
  - Net income before finance income/costs: `545.8` (FY26) / `215.9` (FY25)
  - Average equity: `791.3` (FY26) / `455.4` (FY25)
  - Average borrowings: `120.8` (FY26) / `158.9` (FY25)
  - Return on capital employed: `59.8%` (FY26) / `35.1%` (FY25)
  - Arithmetic: \(545.8 / (791.3 + 120.8) = 545.8 / 912.1 = 59.840\% \to 59.8\%\). FY25: \(215.9 / (455.4 + 158.9) = 215.9 / 614.3 = 35.146\% \to 35.1\%\).
  - Average equity traces to Balance Sheet total equity mean (\((1,035,997 + 546,654)/2 = 791,325.5\)); average borrowings traces to p.44 borrowings mean (\((106.3 + 135.2)/2 = 120.75\)).

---

## 3. Adversarial Findings: Tables Present in PDF but Absent from Build

### 3.1 Dropped Table: Note 18 (Acquisition of Emmerson Resources Limited, p.34)
- **PDF Content**: Physical page 34 contains two major acquisition accounting tables under Note 18.1:
  1. *Purchase Price Table*: Ordinary shares to be issued (102,641,421 shares at GBP1.09) = US\$148,218k + Transaction costs capitalised US\$11,879k = Total acquisition cost **US\$160,097k**.
  2. *Net Assets Allocation Table*: Property, plant and equipment = **US\$142,436k** (Exploration assets 142,244, Buildings leased 112, Other 80) + Investments 86 + Trade receivables 6,427 + Cash 12,796 less Lease liability (133) less Payables (1,515) = Total net assets acquired **US\$160,097k**.
- **Build Failure**: The extractor [`extract_pan_note17_p34.py`](file:///C:/Users/diond/Desktop/Projects/stock_prompts_agentic/workflow/changes/20261029_agentic_report_build/build/extraction/extract_pan_note17_p34.py) applied a modal-width filter to capture 3-column rows and explicitly discarded Note 18's rows, describing them in commit `d99791f` as "a note reference plus a caption fragment ('Ordinary shares to be issued...', 'Property, plant and equipment 7 142,436')".
- **Evidentiary Impact**: A material US\$160.1m transaction is completely missing from `cells`. Furthermore, Note 7 (p.27/28) carries an addition of US\$142,436k from acquisitions, which ties directly to Note 18. This cross-note tie was never executed.

### 3.2 Dropped Section: Note 17.1 Cash-Settled Share Obligation (p.33)
- **PDF Content**: Physical page 33 contains Note 17.1 with a full roll-forward: Opening balance US\$21,486k + P&L expense US\$57,272k + Capitalised expense US\$1,463k less Payments US\$(18,200)k + FX movement = Closing balance.
- **Build Failure**: While raw tokens were captured in `note_p33`, [`test_notes.py`](file:///C:/Users/diond/Desktop/Projects/stock_prompts_agentic/workflow/changes/20261029_agentic_report_build/tests_reconcile/test_notes.py) stops evaluating at line `total_idx` (`Total credit facilities`). Note 17.1 was never reconciled or tied to the Cash Flow Statement (which reports `57,272` expense and `(18,200)` settlement).

### 3.3 Unverified Section: Note 8 Capital Expenditure (p.29)
- **PDF Content**: Physical page 29 contains the IFRS disaggregated Capital Expenditure table:
  - FY26: Sustaining US\$21,832k + Expansion US\$202,163k = Total **US\$223,995k**.
  - FY25: Sustaining US\$11,626k + Expansion US\$156,283k = Total **US\$167,909k**.
- **Build Failure**: Marked `[printed, unverified]` with zero tests. The build relied instead on the rounded APM p.44 numbers (21.8 / 202.2 / 224.0 US\$m) and failed to verify that Note 8 provides the exact dollar grounding for Note 3's capex (223,995 US\$k).

### 3.4 Unverified Section: Note 19 Cash Flow Reconciliation (p.35)
- **PDF Content**: Note 19 details the complete reconciliation from Profit Before Tax (US\$534,368k) to Cash Generated by Operations (US\$556,991k).
- **Build Failure**: Marked unverified with zero executed tests, leaving the Cash Generated from Operations line unanchored to its accounting note.

### 3.5 Omitted Check: Page 50 AISC and AIC Metrics
- Physical page 50 prints `All-in sustainable cost of production` and `All-in cost of production` in ZAR and A\$. The suite does not execute any horizontal sums on these rows, nor does it test cross-table consistency between p.50 AISC and the APM unit tables on pp.42–43.

---

## 4. Recommendations for Next Iteration

1. **Re-extract Note 18 (p.34)**: Write an explicit extractor for Note 18 without modal-width pruning, store the acquisition purchase price and net asset tables, and add a test verifying the US\$142,436k PPE tie between Note 18 and Note 7.
2. **Harmonize Lineage**: Standardize `document` in `cells` to store the SHA-256 hash across all 4,800 rows (replacing the local Windows path in the first 1,196 cells), and populate `extraction_commit` with actual Git commit hashes.
3. **Execute Assertions in the Brief**: Add test assertions in `test_primary_statements.py` for EPS (17.60 / 7.16 cents) and the roll-forward from Profit for the Period to Total Comprehensive Income (US\$400,965k).
4. **Align Brief with Ledger Independence**: Revert the status of `Q-e8c872e6edc94d18` and `Q-a0b503d7ac044eee` in the brief to "Open", distinguishing arithmetic consistency from verified management intent.
