## Section 1 — Key facts and figures

**Trade receivables ECL by ageing (Rm; gross / allowance / net):**

| Date | Current | 30d | 61–90d | >90d | Total | ECL rate |
|---|---|---|---|---|---|---|
| 31 Mar 2026 (unaudited) | 339 / – / 339 | 25 / – / 25 | 5 / – / 5 | 5 / (5) / – | 374 / (5) / 369 | 1.34% |
| 31 Mar 2025 (unaudited)** | 345 / – / 345 | 61 / – / 61 | 6 / – / 6 | 7 / (6) / 1 | 419 / (6) / 413 | 1.43% |
| 30 Sep 2025 (audited) | 286 / <1 / 286 | 52 / <1 / 52 | 15 / (1) / 14 | 11 / (9) / 2 | 364 / (10) / 354 | 2.75% |

- Gross receivables +R10m vs Sep-25 (374 vs 364); net +R15m (369 vs 354) as allowance fell R10m→R5m. YoY: gross −45m, net −44m.
- Ageing mix improved: >90d gross 11→5; 61–90d 15→5; current 286→339.
- **6.2 Currency risk (secondary):** material FX = USD, GBP; exposure mainly foreign-currency receivables realised in ~60 days. FX contracts entered in the period to hedge USD/GBP receipts for Nutun International. Rates (average / closing): USD 16.8/17.2 (Mar-26) vs 18.2/18.4 (Mar-25) vs 18.1/17.3 (Sep-25); GBP 22.4/22.7 vs 23.1/23.9 vs 23.6/23.2; EUR 19.6/19.7; AUD 11.3/11.8.

## Section 2 — Footnotes, qualifications and reconciliations

- **Arithmetic checks (signed):** Mar-26 total allowance: 0+0+0+(−5) = −5 ✓; net 374−5 = 369 ✓. Sep-25: (<1)+(<1)+(−1)+(−9) ≈ −10 ✓; net 364−10 = 354 ✓. Mar-25: −6; net 419−6 = 413 ✓. ECL rates: 5/374 = 1.34% ✓; 6/419 = 1.43% ✓; 10/364 = 2.75% ✓. >90d Mar-26: 5/5 = 100% ✓; Mar-25 6/7 = 85.7% ✓; Sep-25 9/11 = 81.8% ✓.
- **Unit/format flag:** Sep-25 current and 30d allowances printed as "<1" — sub-R1m, not zero; totals use rounded values, so a small rounding residual is possible but not demonstrable.
- **Presentation, not restatement:** footnote * states the ECL-on-trade-receivables disclosure was first presented in the FY2025 AFS (Sep-25) to enhance presentation; ** states the 31 Mar 2025 comparative is presented for the first time. This is a first-time comparative, not evidence of a policy change or unreliable prior reporting.
- **Scope:** single class of trade receivables (no separate classes identified); customers across industries/geographies; ECL based on past default experience, debtor financial position and forward-looking conditions. This is trade-receivable ECL — distinct from PBD/POCI lifetime-loss measurement; do not map these rates onto purchased book debts.
- **Capture boundary:** note starts on shared p.25; 6.2 currency risk likely continues to p.26 (Pending: p.26).

## Section 3 — Questions answered and next evidence

- **Q-29ba2f276efb4af2 (partial):** this section does not address the p.22 "Financial assets subject to risk" table; remains open. No new evidence here.
- **Q-51278219e10b4cd4, Q-c3d790bf20794c50, Q-8612694a3a674266, Q-b67a0f132cee4d6d, Q-75b10eb1d7a24740, Q-9f66f520e55d4b48, Q-73ba5052e544431c, Q-e0ca727b62be46df, Q-e4497d9112cd4e9d, Q-b6d6eda13d854fdf, Q-f8a0c48e3545479f:** not addressed by this capture; carry forward.
- **New questions (see JSON):** (i) reconcile trade-receivable ECL movement (allowance 10→5, gross 364→374) to the cash-flow/income statement and confirm whether the R5m release flows through impairment; (ii) confirm the 6.2 currency-risk continuation on p.26 (hedge notional, maturity, fair value, and whether FX contracts are designated hedges or FVTPL).
- **Next evidence:** Pending: p.26 (6.2 currency risk continuation); D003.11 p.24 and D003.10 p.22 for the PBD/ECL reconciliations.

## Section 4 — Updated Open Questions Ledger

```json
{"ledger_version": 1, "updates": [], "new_questions": [
  {"question": "Reconcile the trade-receivables ECL allowance movement (Sep-25 R10m to Mar-26 R5m; gross 364 to 374; net 354 to 369) to the income statement impairment line and cash-flow statement: is the ~R5m net release recognised in profit or loss, and does the Mar-25 comparative (allowance R6m, gross 419) reconcile to the prior-period impairment charge? Confirm the sub-R1m Sep-25 current/30d allowances are non-zero and state their unrounded values if disclosed.", "priority": "medium", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003.12 p.25; D003.2 income statement (pp.9-11); D003.3 cash-flow (p.12)", "evidence_required": "Trade-receivable ECL charge/release in the income statement and impairment reconciliation, Rm, H1 FY26 vs H1 FY25; unrounded Sep-25 allowance components; confirmation of sign convention (allowance as negative contra-asset)", "closure_condition": "Allowance movement reconciles to the impairment line and cash-flow, or the difference is explicitly identified; benign explanations (rounding, scope) acceptable. Forecast consequence: trade-receivable ECL charge run-rate and working-capital/impairment projection."},
  {"question": "Confirm the 6.2 currency-risk disclosure continuation on p.26: hedge notional amounts, maturities, fair values and whether the USD/GBP FX contracts for Nutun International are designated cash-flow hedges (OCI) or FVTPL; and the split of foreign-currency receivables by currency (USD, GBP, EUR, AUD) at 31 Mar 2026 vs 30 Sep 2025.", "priority": "medium", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003.12 p.26 (6.2 Currency risk continuation)", "evidence_required": "FX hedge notional, maturity, fair value and hedge designation; foreign-currency receivable balances by currency, Rm, at 31 Mar 2026, 31 Mar 2025 and 30 Sep 2025; sensitivity to a 10% FX move if disclosed", "closure_condition": "Hedge designation and notional/fair value disclosed and FX exposure by currency quantified, or confirmed not disclosed; benign explanations (immaterial exposure, hedge accounting not applied) acceptable. Forecast consequence: FX translation/hedging impact on Nutun International earnings and OCI."}
]}
```