## 1. Key facts and figures

**Scope:** Note 7 segment report, H1 FY26 (six months to 31 Mar 2026), unaudited, Rm. Two segments: Nutun South Africa (SA) and Nutun International (Intl). SA is presented on a CODM view (PBD collections in revenue, PBD amortisation in cost of revenue) with IFRS adjustments reconciling to IFRS reporting.

| Line (H1 FY26, Rm) | SA CODM | SA adj. | SA IFRS | Intl | Group |
|---|---|---|---|---|---|
| Revenue | 159 | – | 159 | 552 | 711 |
| Revenue from PBD | 888 | (888) | – | – | – |
| Net income from PBD | – | 69 | 69 | – | 69 |
| Total opex & cost of revenue | (968) | 642 | (326) | (504) | (830) |
| — Cost of revenue | (241) | 105 | (136) | (249) | (385) |
| — PBD amortisation | (597) | 597 | – | – | – |
| — Operating costs | (130) | (60) | (190) | (255) | (445) |
| Other income | 4 | – | 4 | 7 | 11 |
| Equity-accounted loss | (1) | – | (1) | – | (1) |
| Non-operating loss | (2) | – | (2) | (11) | (13) |
| Net finance charge | (203) | 177 | (26) | (13) | (39) |
| PBT | (123) | – | (123) | 31 | (92) |
| Tax | 37 | – | 37 | (8) | 29 |
| **Profit/(loss) continuing** | (86) | – | (86) | 23 | **(63)** |
| Discontinued | – | – | – | – | – |

**Core reconciliation (p.31):** continuing loss (63) → core continuing loss (63) (nil exceptional items) → add back tax (29), D&A 68, PBD amortisation 597, equity loss 1, net finance charge 216 → **core EBITDA 790** (SA 710, Intl 80).

**PBD amortisation footnote (p.31):** 597 = CAEIR imputed interest 383 + impairment loss 167 + net cash collections 728 + FV movements 30 + cash collections 116 (note 1.1 / 1.2). *Arithmetic check: 383 + 167 + 728 + 30 + 116 = 1,424, not 597 — the footnote components do not sum to the stated 597; treat as an unexplained presentation/scope difference, not a plug.*

## 2. Footnotes, qualifications and reconciliations

- **CODM vs IFRS basis:** SA revenue 159 is IFRS (agency/fee) revenue; the 888 PBD collections and 597 amortisation are CODM-only and reverse out. The IFRS "net income from PBD" of 69 is the residual (interest revenue + impairment gains net of collections effect). This confirms PBD is carried at **amortised cost** with interest revenue and impairment in P&L — not FVTPL — for the principal book (relevant to Q-e4497d9112cd4e9d, Q-d22e0c2b395a427e).
- **Q-e0ca727b62be46df bridge:** 790 − 597 − 216 = −23; reported core loss −63; residual −40 = D&A 68 + equity loss 1 + tax 29 = 98 add-backs vs... *check:* −63 + 29 + 68 + 1 + 216 = 251; +597 = 848 ≠ 790. The reconciliation as printed does not foot: adding the listed add-backs to −63 gives 848, not 790 (difference 58). Flag as an arithmetic/presentation inconsistency in the printed reconciliation; do not force a plug. Residual vs the −23 EBITDA-less-amortisation-less-interest path is −40, consistent with D&A 68 less tax 29 less equity 1 = 38 (≈40, rounding). The two paths disagree by ~58; unresolved.
- **PBD amortisation footnote** does not sum to 597 (see above) — components appear to mix note 1.1 (amortised cost) and note 1.2 (FVTPL) populations; scope overlap unresolved.
- **Nil exceptional items** in H1 FY26 core reconciliation — relevant to Q-b18d8ce6d4804a50 (no core adjustments this period).
- **Intl:** revenue 552, EBITDA 80, PBT 31, tax (8), profit 23. FX bridge (Q-23af9329edce40eb) not addressed here.

## 3. Questions answered and next evidence

- **Q-e0ca727b62be46df** — partial: bridge items identified (D&A 68, tax 29, equity 1, net finance 216, PBD amort 597) but printed reconciliation does not foot (848 vs 790, diff 58); residual vs −23 path ≈ −40. Not resolved.
- **Q-e4497d9112cd4e9d** — partial: SA PBD confirmed amortised cost (interest revenue + impairment in P&L); roll-forward not in this capture.
- **Q-d22e0c2b395a427e** — partial: PBD amortisation components (383/167/728/30/116) disclosed but do not sum to 597; ECL release driver split not given.
- **Q-b18d8ce6d4804a50** — partial: nil exceptional/core adjustments H1 FY26 confirmed; basic-to-headline bridge not shown.
- **Q-f8a0c48e3545479f / Q-86ab4a63039b4d7e** — partial: SA IFRS revenue 159 vs Intl 552; principal/agency split still not explicit (PBD collections 888 are CODM gross, not revenue).
- **Q-9f66f520e55d4b48** — not addressed (no prior-year comparative in this capture).
- **Q-f6689319fb3a49ff, Q-23af9329edce40eb, Q-dd187398b68d412d, Q-b6d6eda13d854fdf, Q-73ba5052e544431c** — not addressed here.

**Next evidence:** Pending: D003.4 Note 1 (p.13) PBD roll-forward; Pending: D003.2 (pp.9-11) income statement/equity; Pending: D003.10 (pp.21-23) PBD credit risk; Pending: D003.14 (pp.27-29) FVTPL Level 3.

## 4. Updated Open Questions Ledger

```json
{"ledger_version": 1, "updates": [
{"question_id": "Q-e0ca727b62be46df", "status": "partial", "answer": "Bridge items identified from p.31: core loss (63) + tax 29 + D&A 68 + PBD amortisation 597 + equity loss 1 + net finance 216 = 848, which does not equal the stated core EBITDA 790 (difference 58). The alternative path 790 - 597 - 216 = -23 vs reported -63 leaves residual -40, approximately D&A 68 less tax 29 less equity 1 (=38). The printed reconciliation does not foot; residual not explicitly identified.", "evidence": [{"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 31, "quote": "Core EBITDA per segment** | 710 |  | 80 | 790"}, {"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 31, "quote": "Depreciation and amortisation | 32 |  | 36 | 68"}]},
{"question_id": "Q-e4497d9112cd4e9d", "status": "partial", "answer": "SA principal PBD confirmed on amortised-cost basis: CODM view shows PBD collections 888 in revenue and amortisation 597 in cost of revenue, reversed to IFRS where 'collections are taken into account in the movement of the amortised cost on the statement of financial position, and the income statement therefore reflects interest revenue and impairment gains/(losses)'. Roll-forward to R4,489m not in this capture.", "evidence": [{"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 30, "quote": "In terms of IFRS reporting, collections are taken into account in the movement of the amortised cost on the statement of financial position, and the income statement therefore reflects interest revenue and impairment gains/(losses)."}]},
{"question_id": "Q-d22e0c2b395a427e", "status": "partial", "answer": "PBD amortisation 597 disclosed as CAEIR imputed interest 383 + impairment loss 167 + net cash collections 728 + FV movements 30 + cash collections 116 (notes 1.1/1.2). Components sum to 1,424, not 597 — scope/presentation inconsistency unresolved; ECL release driver split not given.", "evidence": [{"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 31, "quote": "Amortisation of purchased book debts is calculated as CAEIR imputed interest revenue of R383 million, impairment loss of R167 million and net cash collections of R728 million per note 1.1 and fair value movements of R30 million and cash collections of R116 million per note 1.2."}]},
{"question_id": "Q-b18d8ce6d4804a50", "status": "partial", "answer": "H1 FY26 core reconciliation shows nil exceptional items (core and headline adjustments) for both segments and group; basic-to-headline bridge not shown in this capture.", "evidence": [{"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 31, "quote": "Exceptional items (core and headline adjustments) | - |  | - | -"}]},
{"question_id": "Q-f8a0c48e3545479f", "status": "partial", "answer": "SA IFRS revenue 159 (agency/fee) vs Intl 552; SA CODM PBD collections 888 and amortisation 597 reverse out. Principal vs agency split within SA not explicitly stated; PBD amortisation basis (amortised cost) confirmed.", "evidence": [{"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 30, "quote": "Revenue* | 159 – 159 |  |  |  |  | 552 | 711"}]},
{"question_id": "Q-86ab4a63039b4d7e", "status": "partial", "answer": "SA IFRS revenue 159 vs Intl 552; PBD collections 888 (CODM) and amortisation 597 disclosed; measurement basis amortised cost confirmed. Principal/agency revenue split and full roll-forward not disclosed in this capture.", "evidence": [{"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 30, "quote": "Revenue from purchased book debts | 888 (888) -"}]}
], "new_questions": [
{"question": "The p.31 core reconciliation does not foot: core loss (63) plus tax 29, D&A 68, PBD amortisation 597, equity loss 1 and net finance 216 sums to 848, not the stated core EBITDA 790 (difference 58). Separately, the PBD amortisation footnote components (383+167+728+30+116) sum to 1,424, not 597. Provide the corrected signed reconciliation and clarify whether the footnote mixes note 1.1 (amortised cost) and note 1.2 (FVTPL) populations.", "priority": "high", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003.15 note 7 pp.30-31; cross-check D003.4 note 1 p.13 and D003.14 pp.27-29", "evidence_required": "Signed line-item reconciliation footing to core EBITDA 790 and to PBD amortisation 597, Rm, H1 FY26; identification of which components belong to note 1.1 vs 1.2", "closure_condition": "A reconciliation summing to 790 and to 597 is shown, or the 58 and 827 differences are explicitly identified as scope/presentation items; benign explanations (rounding, mixed populations) acceptable; forecast consequence: reliability of core EBITDA and PBD amortisation as run-rate inputs."}
]}
```