# Withholding valuation when material issues remain

A defensible valuation is optional. Report verified historical figures, risks and unresolved questions even when the evidence cannot support a price.

If a material cash-flow, forecast, financing, portfolio, share-count or valuation dependency fails reconciliation or remains unsupported, the result must say:

**VALUATION WITHHELD - MATERIAL ISSUES UNRESOLVED**

Do not publish a target, rating bands, upside, dividend yield, TSR or investment recommendation. These fields must be JSON `null`, not zero, HOLD or an arbitrary distress price. Explain each blocker and the evidence or correction required. Clearly separate conditional scenarios from a published valuation.

## Prompt and output contract

Stage 1 carries forward material FAIL and NOT VERIFIED findings. Stage 2 and SENS prompts use reviewable Stage 1 working claims rather than a 99% confidence baseline. The final material-issue instruction overrides any earlier requirement for a price or numeric summary card.

New output must contain one opening JSON summary with:

- `valuation_status`: `READY` or `WITHHELD`.
- `blocking_issues`: a list of unresolved material issues and required evidence/corrections.
- `valuation_checks`: source evidence and verdicts for the seven dependencies below.
- The usual ticker, company, sector and reference-price fields. Derived valuation fields are populated only when READY.

| Check ID | Required coverage |
| --- | --- |
| historical_cash_flow | Exact statutory subtotal bridged to the chosen cash measure; interest, tax, purchases, capex and leases classified once. |
| forecast_cash_and_debt | Opening balances and flows cover the same period; cash, debt, leases and financing changes reconcile. |
| portfolio_rollforward | Applicable principal and FVTPL portfolios, purchases, collections, income and valuation movements reconcile. |
| valuation_bridge | Components, adjustments, debt, taxes and diluted shares lead to the target without unexplained plugs. |
| sensitivity | Cells use the documented valuation formula and reproduce the central target. |
| earnings_and_shares | Attribution, adjustments, period, shares and cents/rands agree. |
| financing_and_terminal | Debt service, leases, refinancing, dilution and terminal financing match the forecast and discounting basis. |

Each check has `check_id`, `material: true`, an evidence verdict and an `evidence` string identifying sources, physical pages, period, scope and calculations. PASS numerical checks also contain `reconciliations`, each with a label and finite numeric `expected`, `actual` and nonnegative `tolerance` values. The application compares these numbers, even when the check claims PASS. Tolerance must reflect justified rounding.

Allowed verdicts are PASS, FAIL, NOT VERIFIED and NOT APPLICABLE. An exception needs a specific legitimate explanation; a model must not use it to avoid an applicable dependency. Required dependencies cannot be marked immaterial. Routine, supported forecast assumptions remain possible; material missing evidence cannot be disguised as routine uncertainty.

## Application behavior

`section_capture/valuation_policy.py` contains the shared publication policy. New database saves and GUI/CLI/SENS outputs require the readiness contract. Missing, malformed, contradictory or incomplete contracts are withheld. Later/conflicting JSON blocks cannot authorize a price in an earlier scenario block.

Before sanitization, GUI and CLI save exact UTF-8 model responses under `briefs/<period>/candidates/<note-stem>/<UTC-timestamp>.md`. SQLite also retains `stage2_candidate_response`. The public note contains the withholding status and blockers; the preserved candidate remains available for detailed historical analysis and evidence review.

Withholding clears stale target, recommendation, bands and derived return fields. Parent/companion updates preserve each report's own prior baseline. Portfolio and company lists display **Valuation withheld**; dynamic rating fallback cannot recreate a recommendation. The CLI does not recover rejected prices from raw JSON or scenario prose. Its existing material SOTP/guardrail failures also cause withholding, and reruns check these before promoting a candidate.

Historical notes without a readiness contract retain legacy read compatibility. They are not retroactively validated or rewritten. Resaving or resynchronizing such a note is a new publication attempt and requires readiness evidence. Existing NTU notes and price fields were preserved by this implementation; no valuation was rerun.

## What the gate establishes

This is a fail-closed publication decision over declared evidence, reported numerical reconciliations and existing application checks. It does **not** independently prove every source figure, assumption, exception, period label or omitted dependency. A falsely reported PASS or invented matching inputs can still require detection by independent evidence review. READY therefore means the publication prerequisites were met, not that the financial valuation has been independently validated. Continue to follow section 1A of STOCK_EVALUATION_FORMAT.md.

## Approved registry rule

`ALL-MATERIAL-ISSUES-VALUATION-WITHHOLD` applies to all sectors/stages. It is present in the default registry and SQLite. User approval covered this withholding rule and its application enforcement; other proposed analytical amendments remain unimplemented.
