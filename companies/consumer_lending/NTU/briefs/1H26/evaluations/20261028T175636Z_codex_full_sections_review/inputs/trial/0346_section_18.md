## Section 1 | Key facts and figures (D003.13, p.26)

**6.2 Currency risk — foreign-currency monetary balances (Rm, carrying amounts):**

| Currency | Liab 31 Mar 26 | Liab 31 Mar 25 | Liab 30 Sep 25 | Asset 31 Mar 26 | Asset 31 Mar 25 | Asset 30 Sep 25 |
|---|---|---|---|---|---|---|
| USD | 10 | 5 | 1 | 120 | 98 | 135 |
| EUR | – | – | – | 3 | 2 | 3 |
| GBP | 2 | 16 | 1 | 111 | 84 | 78 |
| AUD | – | – | – | – | 6 | 1 |

- Asset footnote: foreign-currency assets = receivables R207m (Mar 25: R171m; Sep 25: R190m) + bank balances R27m (Mar 25: R19m; Sep 25: R27m). **Arithmetic check:** 207 + 27 = 234; table asset total = 120 + 3 + 111 = 234 ✓ (Mar 26). Mar 25: 171 + 19 = 190; table = 98 + 2 + 84 + 6 = 190 ✓. Sep 25: 190 + 27 = 217; table = 135 + 3 + 78 + 1 = 217 ✓. All three dates foot.
- Net open position (assets − liabilities): Mar 26 = 234 − 12 = **+222**; Mar 25 = 190 − 21 = **+169**; Sep 25 = 217 − 2 = **+215**. Net long foreign currency throughout; USD and GBP dominate.
- **6.3 Fair value:** principal book portfolios held at **amortised cost**; fair value approximated by re-discounting risk-adjusted expected cash flows at a current market discount rate of **18.50%** (Mar 25: 15.81%; Sep 25: 15.93%). Stated to approximate carrying value. Interest-bearing liabilities valued via forward curve + consensus margin. Short-term items (receivables, cash, payables, overdrafts) at carrying ≈ fair value.

## Section 2 | Footnotes, qualifications and reconciliations

- The asset footnote reconciles exactly to the table on all three dates (above) — no scope gap.
- **Measurement basis confirmed:** principal book portfolios are **amortised cost**, not FVTPL/POCI. This is directly relevant to the PBD/ECL questions (Q-e4497d9112cd4e9d, Q-d22e0c2b395a427e, Q-51278219e10b4cd4) — the ECL allowance is a conventional amortised-cost allowance, and the 18.50% market discount rate is a fair-value disclosure input, **not** the effective interest rate used for amortisation. Do not conflate the two.
- The 18.50% vs 15.81%/15.93% discount-rate rise is a market-rate observation; the report asserts fair value ≈ carrying value without quantifying the gap. That assertion is unverified here.
- **Capture boundary:** 6.2/6.3 continue; the FX sensitivity analysis and any hedge notionals are **not** in this capture. Pending: D003.13 continuation (pp.27–29).

## Section 3 | Questions answered and next evidence

- **Q-dab8ef060f454ad6** (FX hedge notionals/maturities/sensitivity; confirm units): **partial** — balances by currency now captured (Rm, not R/unit — the table is Rm carrying amounts, resolving the unit ambiguity for *this* table). Hedge notionals, maturities, MTM and sensitivity still not shown. Remains open pending pp.27–29.
- **Q-e4497d9112cd4e9d / Q-d22e0c2b395a427e / Q-51278219e10b4cd4** (PBD measurement basis): **partial** — basis now confirmed as **amortised cost** (p.26). Roll-forward and ECL-release driver split still outstanding (pp.13, 21–24).
- No new material question required beyond carrying the FX-sensitivity/hedge request forward; it is already captured in Q-dab8ef060f454ad6.

**Next evidence:** Pending: D003.13 continuation (pp.27–29) for FX sensitivity/hedges; D003.4 (p.13) and D003.10–11 (pp.21–24) for PBD roll-forward and ECL reconciliation.

## Section 4 | Updated Open Questions Ledger

```json
{"ledger_version": 1, "updates": [{"question_id": "Q-dab8ef060f454ad6", "status": "partial", "answer": "Foreign-currency monetary balances captured (Rm carrying amounts): USD assets 120 / liabilities 10; GBP assets 111 / liabilities 2; EUR assets 3; AUD nil at 31 Mar 2026. Asset footnote reconciles: receivables R207m + bank balances R27m = R234m = table asset total (120+3+111). Net long FX position +R222m (Mar 25 +R169m; Sep 25 +R215m). Table is in Rm carrying amounts, not R/unit. Hedge notionals, maturities, mark-to-market and FX sensitivity are NOT in this capture.", "evidence": [{"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 26, "quote": "US Dollar 10 5 1 120 98 135"}, {"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 26, "quote": "Assets held in foreign currency relate to receivables of R207 million (31 March 2025: R171 million; 30 September 2025: R190 million) and bank balances of R27 million"}]}, {"question_id": "Q-e4497d9112cd4e9d", "status": "partial", "answer": "Measurement basis confirmed: principal book portfolios are held at amortised cost (p.26, 6.3). Fair value is approximated by re-discounting risk-adjusted expected cash flows at a current market discount rate of 18.50% (Mar 25: 15.81%; Sep 25: 15.93%), stated to approximate carrying value. This market rate is a fair-value input, not the EIR used for amortisation. Roll-forward to the R4,489m carrying value still outstanding.", "evidence": [{"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 26, "quote": "Principal book portfolios are held at amortised cost."}, {"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 26, "quote": "current market related discount rate of 18.50% (31 March 2025: 15.81%; 30 September 2025: 15.93%)"}]}, {"question_id": "Q-d22e0c2b395a427e", "status": "partial", "answer": "Measurement basis confirmed as amortised cost (p.26). PBD roll-forward (opening, acquisitions, collections, amortisation, ECL movements, closing) and the split of the R167m ECL release are still not captured; remain outstanding.", "evidence": [{"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 26, "quote": "Principal book portfolios are held at amortised cost."}]}, {"question_id": "Q-51278219e10b4cd4", "status": "partial", "answer": "Basis confirmed amortised cost, so the ECL allowance is a conventional amortised-cost allowance (gross + signed allowance = net). The p.24/p.22/p.8 reconciliation of gross, signed allowance and net carrying value is not in this capture; remains outstanding.", "evidence": [{"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 26, "quote": "Principal book portfolios are held at amortised cost."}]}], "new_questions": []}
```