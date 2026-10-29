# P3 Hypothesis Branches Evaluation Summary

This document records the evaluation of competing interpretations for Section D009 ambiguities,
conducted across isolated Git worktrees and branches per CHARTER §2 (P3) and covenants 1 & 4.

## 1. Branch: `hypothesis/barberton-10k` (worktree `../stock_prompts_hyp_barberton`)
- **Target Ambiguity**: Barberton Mines Total Operations FY26 Gold produced prints as 94,929 oz (p.49 col9), while its printed components are Mining 71,997 oz (col0) + BTRP surface 12,932 oz (col3) = 84,929 oz (Δ +10,000 oz).
- **Hypothesis**: The printed total Operations sum across leaf columns (Barberton 94,929 + Evander 103,330 + MTR 51,927 + Tennant 32,124 = 282,310 oz) exceeds the printed Group total (272,310 oz) by the exact same 10,000 oz. Substituting 84,929 oz makes the operations sum tie the Group total exactly.
- **Evaluation**: Executed in `workflow/changes/20261029_agentic_report_build/tests_reconcile/hypothesis_barberton.py`.
- **Verdict**: **CONDITIONAL AGREEMENT ONLY**.
  - Arithmetic tie confirmed: 84,929 + 103,330 + 51,927 + 32,124 = 272,310.
  - Per Covenant 1, printed 94,929 oz is preserved in `report.sqlite`.
  - Causal origin is unproven (could be an unlisted surface contributor, an accounting adjustment, or a misprint).
  - **Ledger Question `Q-1f48aa6d4b884f09` remains OPEN**.
  - Reconcile test suite status: 15/15 passed.

## 2. Branch: `hypothesis/mtr-buyin` (worktree `../stock_prompts_hyp_mtr`)
- **Target Ambiguity**: In FY25, MTR leaf tailings gold produced prints as 25,043 oz (col6), but MTR Total Operations prints as 30,806 oz (col11), a gap of 5,763 oz (Q-3e8730dbd1994205).
- **Hypothesis**: In FY26, MTR third-party buy-in feedstock is printed as 5,763 oz (col6 and col11). In FY25, buy-in prints as nil ('–') for MTR. The 5,763 oz gap in FY25 represents unlabelled third-party buy-in feedstock embedded into Total Operations.
- **Evaluation**: Executed in `workflow/changes/20261029_agentic_report_build/tests_reconcile/hypothesis_mtr.py`.
- **Verdict**: **ARITHMETIC CONSISTENCY PROVED, CAUSAL CLOSURE UNPROVED**.
  - Arithmetic tie confirmed: 25,043 + 5,763 = 30,806.
  - Surface tailings total also balances: component tailings sum (15,224 + 52,606 + 25,043 = 92,873) + 5,763 = printed 98,636 oz.
  - However, company prose does not state that FY25 experienced 5,763 oz of third-party buy-in or whether the FY26 buy-in figure was mistakenly cross-printed.
  - Per Covenant 4 and prior review corrections, **Ledger Question `Q-3e8730dbd1994205` remains OPEN**.
  - Reconcile test suite status: 15/15 passed.

## Summary Status
Neither hypothesis branch merges changes to printed values onto `agentic-report-build`.
Both branches confirm conditional arithmetic while preserving the printed evidence and keeping ledger questions open.
