# Test coverage by region (self-audit, corrected)

Computed from `report.sqlite` against the test sources. **Method note:** a naive grep for literal
region names under-reports coverage, because `test_notes.py` addresses regions dynamically as
`f"note_p{page}"`. Reading the tests is authoritative; this table is a starting point, not a verdict.

| Region | Cells | Covered | By |
|---|---|---|---|
| A_production, B_costs, C_financial_summary | 1,196 | yes | test_reconciliation.py |
| primary_balance_sheet_assets / equity_liab / income_statement / cash_flows | 192 | yes | test_primary_statements.py |
| note3_segment_analysis | 789 | yes | test_note3_segments.py |
| note3_intra_group | 91 | **no** | deliberately separate block, not a segment grid |
| apm_adjusted_ebitda | 130 | yes | test_apm_ebitda.py |
| apm_aisc_* (4 tables) | 819 | yes | test_apm_aisc.py |
| apm_capital_expenditure, net_debt, net_senior_debt | 98 | yes | test_apm_capital.py |
| apm_nav / levered_fcf / cash_flow_yield | 38 | yes | test_apm_ratios.py |
| apm_roce, per_share_history | 28 | yes | test_apm_roce.py |
| note_p27 (PPE cost) | 238 | yes | test_ppe.py |
| note_p28 (PPE accumulated + carrying) | 224 | yes | test_ppe_accumulated.py |
| **note_p25 (Note 4 revenue)** | 90 | **yes** | test_notes.py (dynamic region name) |
| **note_p32 (Note 16 borrowings)** | 74 | **yes** | test_notes.py (dynamic region name) |
| **note_p33 (Note 16.7 facilities)** | 62 | **yes** | test_notes.py (dynamic region name) |
| note_p4, 6, 9, 10, 19, 26, 29, 30, 31, 34, 35, 36, 39 | 822 | **no** | extracted, values + lineage only |

**Totals**: 3,978 cells covered (82.9%) · **822 cells uncovered (17.1%)** across 14 regions ·
1,048 is the figure a naive grep produces and it is wrong by 226 cells.

## What the uncovered 822 cells represent

- **`note3_intra_group` (91)** — the elimination block on pp.21/23. Excluded by design; it has no
  segment-column semantics. Recorded as a conflict.
- **13 note/front pages (731)** — printed values with page, hash and commit, but **no established column
  meaning**: `fiscal_year` is NULL and `column_index` is printed position. No identity has been executed.
  The brief marks these `[printed, unverified]`.

## What a reviewer should do with this

Do not re-check the covered rows — 109 tests already do. Spend effort on the 822:

1. For each uncovered page, read the printed header and decide what the columns mean.
2. Then ask which of those pages *should* have a checkable identity (tax reconciliation, cash-generated-
   from-operations bridge, capex note) and whether the absence of a test is justified.
3. Any figure cited in `READING_BRIEF_CONSOLIDATED.md` that traces to an uncovered region is a finding,
   because the brief claims no conclusion rests on unverified rows.
