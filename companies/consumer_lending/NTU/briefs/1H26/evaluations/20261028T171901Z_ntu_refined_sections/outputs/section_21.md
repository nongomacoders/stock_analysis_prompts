## 1. Key facts and figures

**Scope:** D003.16 supplies only the **H1 2025 comparative** segment/core reconciliation (physical pp. 32–33; printed pages 30–31). H1 2026 segment figures are in D003.15 (pp. 30–31) — **not supplied here**. All figures Rm, unaudited, half year ended 31 Mar 2025.

| Item (H1 2025) | Nutun SA | Nutun Intl | Group |
|---|---|---|---|
| Revenue (excl. PBD) | 188 | 557 | 745 |
| Revenue from PBD (CODM) | 694 | – | – |
| Net income from PBD (IFRS) | 53 | – | 53 |
| Total opex & cost of revenue (IFRS) | (398) | (514) | (912) |
| Operating (loss)/profit | (202) | 41 | (161) |
| Continuing (loss)/profit | (155) | 33 | (122) |
| Discontinued profit | 58 | – | 58 |
| **Total (loss)/profit** | (97) | 33 | **(64)** |
| Core continuing (loss)/earnings | (104) | 33 | **(71)** |
| **Core EBITDA** | 522 | 93 | **615** |
| Core discontinued loss | – | – | **–** |

- **Core reconciliation (p.33):** continuing loss (122) + exceptional 51 + transaction costs 5 + tax (1) + associate impairment 47 = core continuing loss **(71)**. Check: −122+51+5−1+47 = −20… **does not foot** — see §2.
- **Core EBITDA build:** core loss (71) + tax (38) + D&A 73 + PBD amortisation 422 + equity loss (4) + net finance 233 = **615**. Check: −71−38+73+422−4+233 = 615 ✓.
- **Discontinued:** profit 58 − exceptional (58) + disposal profit (100) + tax 29 + transaction 16 − tax (3) = **0** ✓ (core discontinued nil).
- **PBD amortisation 422** = CAEIR imputed interest 333 + impairment loss 173 − net cash collections 566 + FV movements 74 + cash collections 90 (note 4). Check: 333+173−566+74+90 = 104 ≠ 422 — **does not foot**; see §2.

## 2. Footnotes, qualifications and reconciliations

- **Core continuing reconciliation does not foot as captured.** Stated components sum to −20, not −71 (residual −51). The "Exceptional items 51" line appears to be the reconciling total, with transaction costs 5, tax (1) and associate impairment 47 as its sub-components (5−1+47 = 51). If so, the 51 is a subtotal, not an additive line — the table layout is ambiguous. Flagged, not resolved.
- **PBD amortisation note (footnote 4) does not foot** to the 422 charged: components sum to 104. Either the note lists only part of the amortisation, or signs/scope differ (e.g. 333 and 173 may be gross-of-something). Unresolved; do not plug.
- **"Comparative presented for the first time"** (both p.33 tables): this is a first-time presentation of H1 2025 comparatives, **not** a restatement or policy change. No reliability inference should be drawn.
- **Core EBITDA** is explicitly non-IFRS (management's view of operating cash flows) — not comparable to IFRS operating profit.
- **Segment column mapping:** p.32 header is garbled (CODM/IFRS/adjustments columns). IFRS Group revenue 745 = 188 + 557 ✓; IFRS Group opex (912) = (398)+(514) ✓. CODM PBD revenue 694 is eliminated to net income 53 via (694)+422 amortisation+… — the CODM→IFRS bridge is only partly visible.

## 3. Questions answered and next evidence

- **Q-e0ca727b62be46df (partial):** H1 2025 bridge now visible: core loss (71) → EBITDA 615 via tax (38), D&A 73, PBD amort 422, equity (4), net finance 233 (foots ✓). The earlier −23→−63 residual was an H1 2026 issue (D003.15, not supplied). H1 2025 side resolved; H1 2026 side still open.
- **Q-b18d8ce6d4804a50 (partial):** H1 2025 core/headline adjustments identified: exceptional 51 (restructuring), transaction costs 5, associate impairment 47, tax (1); discontinued: disposal profit (100), transaction 16, tax 29/(3). H1 2026 adjustments not in this capture.
- **Q-86ab4a63039b4d7e / Q-f8a0c48e3545479f (partial):** PBD amortisation basis partly shown (CAEIR 333, impairment 173, collections 566, FV 74, cash 90) but does not foot to 422; principal/agency split still not disclosed.
- **Q-9f66f520e55d4b48 / Q-f8db08b395c448a9:** SA revenue H1 2025 = 188 confirmed (matches Note 4 comparative); direction vs H1 2026 (159) still to confirm from D003.15.
- **New questions:** core reconciliation footing (p.33); PBD amortisation footnote footing (p.33); H1 2026 segment/core figures (D003.15).

**Next evidence:** D003.15 (pp. 30–31) for H1 2026 segment/core figures; D003.4 (p.13) and D003.10 (pp.21–23) for PBD roll-forward; D003.2 (pp.9–11) for headline EPS bridge.

## 4. Updated Open Questions Ledger

```json
{"ledger_version": 1, "updates": [
{"question_id": "Q-e0ca727b62be46df", "status": "partial", "answer": "H1 2025 side now reconciles: core continuing loss (71) + tax (38) + D&A 73 + PBD amortisation 422 + equity loss (4) + net finance 233 = core EBITDA 615 (foots). H1 2026 bridge (the -23 to -63 residual) is in D003.15, not supplied here.", "evidence": [{"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 33, "quote": "Core EBITDA per segment* | 522 |  |  | 93 | 615"}]},
{"question_id": "Q-b18d8ce6d4804a50", "status": "partial", "answer": "H1 2025 core/headline adjustments: exceptional items 51 (restructuring), transaction costs 5, tax (1), associate impairment 47; discontinued: disposal profit (100), transaction costs 16, tax 29 and (3). H1 2026 adjustments not in this capture.", "evidence": [{"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 33, "quote": "Impairment of investment in associate | 2 47"}]},
{"question_id": "Q-86ab4a63039b4d7e", "status": "partial", "answer": "PBD amortisation basis partly disclosed (footnote 4): CAEIR imputed interest 333, impairment loss 173, net cash collections 566, FV movements 74, cash collections 90 — but these sum to 104, not the 422 charged. Principal/agency revenue split still not disclosed.", "evidence": [{"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 33, "quote": "Amortisation of purchased book debts is calculated as CAEIR imputed interest revenue of R333 million, impairment loss of R173 million and net cash"}]},
{"question_id": "Q-f8a0c48e3545479f", "status": "partial", "answer": "PBD amortisation components partly shown (see Q-86ab4a63039b4d7e) but do not foot to 422; principal/agency split and full roll-forward not disclosed in this capture.", "evidence": [{"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 33, "quote": "Amortisation of purchased book debts | 4 422"}]},
{"question_id": "Q-9f66f520e55d4b48", "status": "partial", "answer": "H1 2025 Nutun SA revenue confirmed at 188 (matches Note 4 comparative); H1 2026 figure (159) and driver not in this capture.", "evidence": [{"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 32, "quote": "Revenue* | 188 – 188"}]}
], "new_questions": [
{"question": "The p.33 core continuing reconciliation does not foot as captured: (122)+51+5+(1)+47 = -20, not the stated core loss of (71). Confirm whether 'Exceptional items 51' is a subtotal of the following lines (transaction costs 5, tax (1), associate impairment 47) rather than an additive line, and provide the corrected signed bridge for H1 2025 and H1 2026.", "priority": "high", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003.16 p.33 (and D003.15 p.30-31 for H1 2026)", "evidence_required": "Corrected line-item core reconciliation (Rm) footing to core continuing loss (71) H1 2025 and the H1 2026 equivalent, with column/indent mapping clarified", "closure_condition": "A signed bridge summing to (71) (and H1 2026 core loss) is shown, or the layout ambiguity is confirmed as a capture artefact; benign explanation (subtotal presentation) acceptable. Forecast consequence: reliability of core earnings as run-rate base."},
{"question": "PBD amortisation footnote 4 components (CAEIR 333 + impairment 173 - net collections 566 + FV 74 + cash 90) sum to 104, not the 422 amortisation charged. Reconcile the footnote to the 422 line and state whether components are gross/net and which portfolios (note 1.1 vs 1.2) they cover.", "priority": "high", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003.16 p.33 footnote 4; cross-check D003.4 p.13 and D003.10 pp.21-23", "evidence_required": "Signed reconciliation of footnote 4 components to 422 amortisation, Rm, H1 2025 and H1 2026, with portfolio scope and gross/net basis", "closure_condition": "Footnote components reconcile to 422 (or the difference is explicitly identified); benign explanation (partial listing, sign convention) acceptable. Forecast consequence: PBD amortisation projection."},
{"question": "Provide the H1 2026 segment and core reconciliation (Nutun SA, Nutun International, Group) equivalent to the H1 2025 tables on pp.32-33, including core continuing earnings, core EBITDA and core discontinued loss, to complete the H1 2026 vs H1 2025 comparison.", "priority": "high", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003.15 pp.30-31", "evidence_required": "H1 2026 segment income statement and core reconciliation tables, Rm, footing to core EBITDA and core continuing loss", "closure_condition": "H1 2026 tables supplied and footing; forecast consequence: run-rate core earnings and segment EBITDA."}
]}
```