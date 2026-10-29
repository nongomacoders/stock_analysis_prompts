## Section 1 — Key facts and figures

**D003.11 (p.24) — ECL allowance reconciliation, principal book portfolios, Rm**

| Line | Banking & specialised lending – Debt review | Unsecured Retail | (col.3, unlabelled) | Banking – Secured | Total |
|---|---|---|---|---|---|
| Balance 30 Sep 2024 (audited) | 575 | 148 | 30 | 44 | 797 |
| Impairment (loss)/gain on principal book | (115) | (83) | 24 | 1 | (173) |
| — of which acquired during period | (51) | (45) | – | – | (96) |
| — of which historical portfolios | (64) | (38) | 24 | 1 | (77) |
| Balance 31 Mar 2025 (unaudited)** | 460 | 65 | 54 | 45 | 624 |
| Impairment gain/(loss) on principal book | 8 | 7 | (7) | (34) | (26) |
| — acquired during period | 66 | 89 | 1 | – | 156 |
| — historical portfolios | (58) | (82) | (8) | (34) | (182) |
| Balance 30 Sep 2025 (audited) | 468 | 72 | 47 | 11 | 598 |
| Impairment (loss)/gain on principal book | (241) | 69 | 4 | 1 | (167) |
| — acquired during period | 1 | 23 | – | – | 24 |
| — historical portfolios | (242) | 46 | 4 | 1 | (191) |
| Balance 31 Mar 2026 (unaudited) | 227 | 141 | 51 | 12 | 431 |

- **Sign convention:** the balance is a *cumulative impairment gain* (contra-asset / negative allowance), not a loss reserve. A negative movement line reduces the gain (i.e. increases net carrying value); a positive line increases the gain. The narrative confirms "cumulative impairment gain of R431 million."
- **Arithmetic checks (all foot):** 797 − 173 = 624; 624 − 26 = 598; 598 − 167 = 431. Column sums: 575+148+30+44 = 797; 460+65+54+45 = 624; 468+72+47+11 = 598; 227+141+51+12 = 431. Sub-splits: (51)+(64) = (115); (45)+(38) = (83); 24 = 24; (96)+(77) = (173). H1 FY26: 1+(242) = (241); 23+46 = 69; 4 = 4; 24+(191) = (167).
- **Driver (management explanation):** H1 FY26 net loss of R241m in Debt review (historical −242) drives the total reduction of the gain from 598 → 431. Narrative attributes the reduction to "payer drop-offs and reduced settlement activity on historical book portfolios." Unsecured Retail gain rose 72 → 141 (acquired +23, historical +46).
- **Periods/basis:** H1 FY26 (31 Mar 2026) vs FY25 (30 Sep 2025) vs H1 FY25 (31 Mar 2025); Rm; unaudited interim, audited year-ends.

## Section 2 — Footnotes, qualifications and reconciliations

- **\* First-time presentation:** the reconciliation was first presented in the FY25 AFS "to enhance overall presentation." This is a presentation change, not a restatement of balances.
- **\*\* Comparative first-time:** the 31 Mar 2025 column is presented for the first time; it is a new comparative, not evidence of a policy change or prior misstatement.
- **Unlabelled third column:** the header row shows only three column labels ("Banking & specialised lending – Debt review", "Unsecured Retail", "Banking – Secured", "Total") but four numeric columns. The third column (30 → 54 → 47 → 51) is unlabelled in the capture. Its identity is unresolved — do not assume it is a segment; flag as a capture/layout ambiguity.
- **Scope vs p.22 question (Q-29ba…):** this table reconciles the *allowance/gain* only, not gross carrying value or net book. It does not by itself resolve the p.22 footing/sign issue; it does corroborate that the principal-book allowance is a signed cumulative gain (contra), consistent with "net = gross + allowance" if allowance is negative.
- **No gross/net or coverage ratios** are given here; cannot compute coverage from this page alone.

## Section 3 — Questions answered and next evidence

- **Q-29ba2f276efb4af2 (partial):** confirms the principal-book allowance is a signed cumulative *gain* (contra-asset), supporting "net = gross + allowance" with a negative allowance. Does **not** reconcile the p.22 Total column (9,879 vs 4,884) — remains open. Pending: D003.10 p.22.
- **Q-d22e0c2b395a427e / Q-e4497d9112cd4e9d / Q-86ab4a63039b4d7e / Q-f8a0c48e3545479f (partial):** this page gives the ECL-gain movement split (acquired vs historical) by portfolio, but **not** the PBD roll-forward (acquisitions, collections, amortisation) or principal-vs-agency revenue split. Those remain open. Pending: D003.4 p.13; D003.10 pp.21–23.
- **New questions (see JSON):** identity of the unlabelled third column; reconciliation of this allowance movement to the p.22 net carrying values and to the R167m ECL release referenced in stored questions (598 → 431).

Next evidence: D003.10 pp.21–23 (PBD tables, column labels, gross/net); D003.4 p.13 (PBD roll-forward); D003.1 p.8 (carrying values).

## Section 4 — Updated Open Questions Ledger

```json
{"ledger_version": 1, "updates": [{"question_id": "Q-29ba2f276efb4af2", "status": "partial", "answer": "D003.11 (p.24) confirms the principal-book ECL allowance is a signed cumulative impairment GAIN (contra-asset), so net carrying value = gross + (negative) allowance. It does not reconcile the p.22 Total column (components 9,879 vs printed 4,884); that footing/sign issue remains open pending p.22.", "evidence": [{"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 24, "quote": "The cumulative impairment gain of R431 million relates to elevated performance, above the investment base-case"}]}, {"question_id": "Q-d22e0c2b395a427e", "status": "partial", "answer": "D003.11 gives the ECL-gain movement split (acquired vs historical) by portfolio for H1 FY26 and H1 FY25, and confirms the 598 to 431 reduction (net -167; historical -191, acquired +24). It does NOT provide the PBD roll-forward (acquisitions, collections, amortisation) or reconcile to principal-book net carrying values; those remain open.", "evidence": [{"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 24, "quote": "The reduction in the cumulative impairment gain in the current year relates to payer drop-offs and reduced settlement activity on historical book portfolios"}]}, {"question_id": "Q-e4497d9112cd4e9d", "status": "partial", "answer": "D003.11 shows the allowance is a cumulative impairment gain (contra), consistent with a POCI-style measurement where lifetime expected losses are below the investment base-case. Measurement basis label and full roll-forward to the R4,489m carrying value are not on this page; remain open.", "evidence": [{"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 24, "quote": "Reconciliation of expected credit loss allowance on principal book portfolios*"}]}], "new_questions": [{"question": "Identify the unlabelled third numeric column in the D003.11 ECL reconciliation (values 30, 54, 47, 51 across the four dates) and confirm the full column-header mapping for all four portfolio columns plus Total. Is this a segment, a portfolio type, or a capture/layout artefact?", "priority": "medium", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003.11 p.24; cross-check D003.10 pp.21-23", "evidence_required": "Full column headers for the ECL reconciliation table (all four portfolio columns and Total) as printed, Rm, at 31 Mar 2026, 30 Sep 2025, 31 Mar 2025 and 30 Sep 2024", "closure_condition": "Each column is labelled and the Total foots to the sum of labelled columns, or the unlabelled column is confirmed as a capture artefact; benign explanations (layout/OCR) acceptable. Forecast consequence: correct segment attribution of ECL movements."}, {"question": "Reconcile the D003.11 ECL-gain movement (598 to 431, net -167) to the p.22 principal-book net carrying values and to the R167m ECL release referenced in stored questions: confirm the allowance is the same signed quantity and that gross carrying value plus this allowance equals the reported net carrying value at 31 Mar 2026 and 30 Sep 2025.", "priority": "high", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003.11 p.24; D003.10 p.22; D003.1 p.8", "evidence_required": "Gross carrying value, signed ECL allowance/gain and net carrying value for principal book portfolios, Rm, at 31 Mar 2026 and 30 Sep 2025, footing to the statement of financial position", "closure_condition": "Gross + signed allowance = net carrying value reconciles across p.24, p.22 and p.8, or the difference is explicitly identified; benign explanations (scope, rounding) acceptable. Forecast consequence: correct ECL base and net PBD value for projection."}]}
```