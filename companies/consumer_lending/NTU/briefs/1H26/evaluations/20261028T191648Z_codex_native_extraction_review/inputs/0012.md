## Section 1. Key facts and figures

**D003.12 — ECL allowance on trade receivables (p.25, Rm; gross / allowance / net):**

| Bucket | 31 Mar 2026 (unaudited) | 31 Mar 2025 (unaudited) | 30 Sep 2025 (audited) |
|---|---|---|---|
| Current | 339 / – / 339 | 345 / – / 345 | 286 / <1 / 286 |
| 30 days overdue | 25 / – / 25 | 61 / – / 61 | 52 / <1 / 52 |
| 61–90 days overdue | 5 / – / 5 | 6 / – / 6 | 15 / (1) / 14 |
| 90+ days overdue | 5 / (5) / – | 7 / (6) / 1 | 11 / (9) / 2 |
| **Total** | **374 / (5) / 369** | **419 / (6) / 413** | **364 / (10) / 354** |

- Total ECL rate: 1.34% (Mar-26), 1.43% (Mar-25), 2.75% (Sep-25). 90+ loss rate: 100% (Mar-26), 85.71% (Mar-25), 81.82% (Sep-25).
- Gross receivables fell 10.7% vs Mar-25 (374 vs 419) and rose 2.7% vs Sep-25 (374 vs 364); allowance fell from 10 to 5.
- **6.2 Currency risk (secondary, p.25):** material FX exposure USD and GBP, largely foreign-currency receivables realised in 60 days; Nutun entered FX contracts in the period to hedge USD/GBP receipts for the Nutun International segment. Closing rates: USD 17.2 (Mar-26) vs 18.4 (Sep-25) / 17.3 (Mar-25); GBP 22.7 vs 23.9 / 23.2; EUR 19.7 vs 20.0 / 20.0; AUD 11.8 vs 11.6 / 11.4. Average rates: USD 16.8 vs 18.2 / 18.1.

## Section 2. Footnotes, qualifications and reconciliations

- **Arithmetic checks (foot):** Mar-26 gross 339+25+5+5 = 374 ✓; allowance 0+0+0+5 = 5 ✓; net 369 ✓. Mar-25: 345+61+6+7 = 419 ✓; allowance 6 ✓; net 413 ✓. Sep-25: 286+52+15+11 = 364 ✓; allowance <1+<1+1+9 ≈ 10 ✓; net 354 ✓. Bucket loss rates are consistent with printed allowances (e.g. Mar-26 90+: 5/5 = 100%; Sep-25 61–90: 1/15 = 6.67%).
- **Unit/format ambiguity:** the header row is garbled ("Amounts Amounts in excess of / 30 days 61 to 90 days / 90 days overdue") and the currency row prints "Rm" for what are clearly exchange rates (USD 16.8 etc.). Treat the FX table as **R per unit of foreign currency**, not Rm — a capture/label artefact, not a report rescaling. Flagged, not corrected.
- **First-time presentation:** footnote * states the ECL-by-maturity disclosure was first presented in the FY2025 AFS (Sep-25 audited); footnote ** states the Mar-25 comparative is presented for the first time. This is an **enhanced-disclosure change, not a restatement** — the Mar-25 figures are new comparative presentation, not a prior-period correction. Do not infer policy change or unreliability.
- **Scope:** no separate trade-receivable classes identified; credit risk managed on past default experience, debtor-specific factors and forward-looking conditions. This is a **conventional IFRS 9 trade-receivable ECL table** — distinct from the POCI/purchased-book-debt measurement in D003.10–D003.11; do not conflate the two allowance bases.
- **Coverage gap:** the 90+ bucket is fully provided at Mar-26 (100%) but only 85.71% at Mar-25 and 81.82% at Sep-25 — a genuine tightening, but the driver (ageing mix vs assumption change) is not disclosed here.
- **Continuation:** 6.2 Currency risk continues beyond this capture (FX contracts, sensitivity) — Pending: p.26.

## Section 3. Questions answered and next evidence

- **Q-29ba2f276efb4af2 (p.22 financial-assets table):** not addressed by this page — remains **partial/open**. This page's trade-receivable table foots cleanly; it does not resolve the p.22 principal-book sign/column issue.
- **Q-51278219e10b4cd4 / Q-e4497d9112cd4e9d (PBD ECL reconciliation):** not addressed — this is trade receivables, a different scope from principal-book PBD. Remain open.
- **Q-c3d790bf20794c50, Q-8612694a3a674266, Q-b67a0f132cee4d6d, Q-75b10eb1d7a24740, Q-9f66f520e55d4b48, Q-73ba5052e544431c, Q-e0ca727b62be46df, Q-f8a0c48e3545479f:** not addressed by p.25 — carry forward unchanged.
- **New material questions (see JSON):** (i) driver of the 90+ coverage step-up to 100% and allowance fall 10→5 despite gross rising vs Sep-25; (ii) FX hedge notional/maturity and sensitivity for the Nutun International USD/GBP receipts (6.2 continuation, p.26).

Next evidence: p.26 (6.2 Currency risk continuation — FX contract notionals, maturities, sensitivity); Pending: D003.10–D003.11 (pp.21–24) for PBD ECL reconciliation.

## Section 4. Updated Open Questions Ledger

```json
{"ledger_version": 1, "updates": [], "new_questions": [
  {"question": "What drove the trade-receivable 90+ days loss allowance to 100% coverage at 31 Mar 2026 (from 85.71% at 31 Mar 2025 and 81.82% at 30 Sep 2025), and why did total allowance fall from R10m (Sep-25) to R5m (Mar-26) while gross receivables rose from R364m to R374m? Split the movement between ageing/volume mix and forward-looking assumption changes.", "priority": "medium", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003.12 p.25 (ECL on trade receivables); cross-check D003.9 credit risk (p.20) and D003.10 (pp.21-23)", "evidence_required": "Trade-receivable ECL roll-forward (opening, charge/release, write-offs, closing) in Rm for H1 FY26 and H1 FY25; ageing migration; statement of the forward-looking assumptions and any change in provisioning policy for 90+ days; reconciliation of the R10m to R5m allowance movement", "closure_condition": "Driver of the 90+ coverage step-up and the allowance decline is disclosed or explicitly identified, or confirmed not disclosed; benign explanations (ageing mix, write-offs, assumption change) acceptable. Forecast consequence: trade-receivable ECL charge and working-capital/credit-loss projection."},
  {"question": "What are the notional amounts, maturities and mark-to-market of the USD/GBP foreign-exchange contracts entered into to hedge Nutun International receipts, and what is the disclosed FX sensitivity? Confirm the FX table units are R per unit of foreign currency (not Rm).", "priority": "medium", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003.12 p.25-26 (6.2 Currency risk continuation)", "evidence_required": "FX hedge notional, maturity profile and fair value (Rm) at 31 Mar 2026; FX sensitivity analysis; confirmation of exchange-rate units; foreign-currency receivable balances by currency", "closure_condition": "Hedge notionals/maturities and sensitivity disclosed, or confirmed not disclosed; benign explanations (immaterial, disclosed elsewhere) acceptable. Forecast consequence: FX translation and hedging impact on Nutun International earnings."}
]}
```