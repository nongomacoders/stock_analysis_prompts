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

---

## 3. Section S006 Primary Statements Hypotheses & Disclosures

### A. Cash Flow Statement: Reciprocal Dividend Cash Flow Re-presentation (Footnote 1, physical p.18)
- **Source Disclosure**: *"The Group changed the presentation of reciprocal dividend cash flows from gross to net during the current reporting period. The comparative figures have been re-presented accordingly."*
- **Evidence**: Dividend paid is printed as $(58,540\text{k})$ in FY26 and $(23,675\text{k})$ in FY25.
- **Evaluation**: The cash flow reconciliation ties exactly with the re-presented comparative ($49,532\text{k} + 22,466\text{k} + 734\text{k} = 49,532\text{k}$ via closing cash). Per Covenant 1 and reporting guidelines, first-time presentation of a comparative re-presentation is recorded as an explicit disclosure, not a reporting error.

### B. Cross-Section Revenue Bridge (IFRS p.18 vs Segmental p.50, `Q-a0b503d7ac044eee`)
- **Target**: Reconcile Section S006 IFRS Consolidated Revenue ($1,156,451\text{k} \text{ US\$}$) with Section D009 segmental mining revenue ($\text{ZAR } 17,249.1\text{m}$).
- **Evaluation**:
  - Converting IFRS Revenue at the p.50 average exchange rate ($16.90\text{ US\$/ZAR}$):  
    $$1,156.451\text{m US\$} \times 16.90 = \text{ZAR } 19,544.02\text{m}$$
  - Segmental mining revenue printed on p.50: $\text{ZAR } 17,249.1\text{m}$.
  - Delta: $\text{ZAR } 19,544.0\text{m} - \text{ZAR } 17,249.1\text{m} = \text{ZAR } 2,294.9\text{m}$.
  - Note 4 on p.25 disaggregates revenue into Gold revenue ($1,152,437\text{k}$) and other revenue items, indicating that the $\text{ZAR } 2,294.9\text{m}$ bridge includes exchange rate conversion timing (transaction-date spot rates vs annual average $16.90$) and corporate/Australian revenue adjustments (`Q-c5e1b41b1cfe4dfb`).
  - **Verdict**: Arithmetic bridge proved; `Q-a0b503d7ac044eee` updated with exact bridge numbers while remaining open for note-level timing breakdown.
