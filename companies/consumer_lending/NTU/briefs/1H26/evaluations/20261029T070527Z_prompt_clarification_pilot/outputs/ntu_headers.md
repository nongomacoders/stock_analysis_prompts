## Section 1 | Key facts and figures

**Scope:** D003.11 (p.24) is the ECL allowance reconciliation on **principal book portfolios** (owned NPL books), split by four segments. It is a **cumulative impairment gain** presentation — the R431m closing balance is a *credit balance* (gain) against the acquired book, not a conventional ECL reserve. This is the POCI-style measurement the sector note flags: a *decrease* in the cumulative gain is an impairment loss.

| Segment (Rm) | 30 Sep 24 (A) | 31 Mar 25 (U) | 30 Sep 25 (A) | 31 Mar 26 (U) |
|---|---|---|---|---|
| Banking & specialised lending – Unsecured | 575 | 460 | 468 | 227 |
| Debt review | 148 | 65 | 72 | 141 |
| Retail | 30 | 54 | 47 | 51 |
| Banking – Secured | 44 | 45 | 11 | 12 |
| **Total** | **797** | **624** | **598** | **431** |

**H1 FY26 movement (598 → 431, net −167):**
- Acquired-book gain: **+24** (Unsecured +1; Debt review +23)
- Historical-book loss: **−191** (Unsecured −242; Debt review +46; Retail +4; Secured +1)
- Check: 24 − 191 = **−167**; 598 − 167 = **431** ✓ (foots)

**H1 FY25 movement (797 → 624, net −173):**
- Acquired-book loss: **−96** (Unsecured −51; Debt review −45)
- Historical-book loss: **−77** (Unsecured −64; Debt review −38; Retail +24; Secured +1)
- Check: −96 − 77 = **−173**; 797 − 173 = **624** ✓

**H2 FY25 movement (624 → 598, net −26):**
- Acquired-book gain: **+156** (Unsecured +66; Debt review +89; Retail +1)
- Historical-book loss: **−182** (Unsecured −58; Debt review −82; Retail −8; Secured −34)
- Check: 156 − 182 = **−26**; 624 − 26 = **598** ✓

**Driver (management explanation):** cumulative gain reflects performance above investment base-case, predominantly Banking & Specialised Lending. Current-year reduction attributed to **payer drop-offs and reduced settlement activity on historical books**.

## Section 2 | Footnotes, qualifications and reconciliations

- **Footnote \*:** disclosure first presented in FY25 AFS "to enhance overall presentation" — a presentation change, not a restatement.
- **Footnote \*\*:** 31 Mar 25 comparative presented for the first time. Per the prompt's rule, first-time comparative presentation alone does **not** establish a restatement or policy change; no explicit restatement is disclosed.
- **Sign convention:** the table is a *cumulative impairment gain* (positive = gain). The "Impairment (loss)/gain" line is signed; the acquired/historical split sums to the total line in every period (verified above). A **decrease** in the balance is an impairment loss, not a reserve release — do not read the 598→431 fall as a "release."
- **Segment volatility:** Debt review swings 148→65→72→141; Secured 44→45→11→12. The Unsecured book carries the bulk of the historical-book loss (−242 in H1 FY26). These are large relative moves on small bases — flag for credit-quality follow-up.
- **Unresolved:** the table gives no gross carrying value, no split of the acquired-book gain between model/assumption change and collections, and no reconciliation to the p.22 "Financial assets subject to risk" table or the statement of financial position. Cannot confirm the R431m ties to any balance-sheet line from this capture alone.

## Section 3 | Questions answered and next evidence

- **Q-29ba2f276efb4af2** (p.22 table footing/sign): **partial** — this section confirms the *sign convention* for the principal-book ECL (cumulative gain, positive = gain; decrease = loss), which is the likely source of the "gross + allowance" confusion. But the p.22 Total-column footing (9,879 vs 4,884) is **not** resolved here; p.22 not in this capture. Pending: D003.10 p.22.
- **Q-d22e0c2b395a427e / Q-e4497d9112cd4e9d / Q-f8a0c48e3545479f / Q-86ab4a63039b4d7e** (PBD roll-forward, measurement basis, ECL release driver split): **partial** — this section supplies the **ECL allowance movement** (598→431, split acquired +24 / historical −191) and the qualitative driver (payer drop-offs, reduced settlements). It does **not** supply the full PBD roll-forward (acquisitions, collections, amortisation) or the measurement-basis label. Pending: D003.4 p.13; D003.10 pp.21–23.
- **Q-e0ca727b62be46df** (EBITDA→core loss bridge): not addressed here.
- **Q-8612694a3a674266 / Q-75b10eb1d7a24740 / Q-b6d6eda13d854fdf / Q-b67a0f132cee4d6d** (overdraft/facilities/covenants): not addressed here.
- **Q-9f66f520e55d4b48** (SA revenue direction): not addressed here.
- **Q-73ba5052e544431c** (treasury shares): not addressed here.

**New question (see ledger):** reconcile the R431m cumulative gain to the p.22 principal-book net carrying value and confirm whether the acquired-book +24 gain is a POCI measurement gain (not an ECL reserve movement), with the gross carrying value and the model-vs-collections split.

**Next evidence:** D003.10 pp.21–23 (PBD detail, p.22 table); D003.4 p.13 (Note 1); D003.1 p.8 (SoFP).

## Section 4 | Updated Open Questions Ledger

```json
{"ledger_version": 1, "updates": [{"question_id": "Q-29ba2f276efb4af2", "status": "partial", "answer": "D003.11 (p.24) confirms the principal-book ECL is presented as a cumulative impairment GAIN (positive = gain; a decrease is an impairment loss, not a reserve release). This likely explains the 'gross + allowance' sign confusion. The p.22 Total-column footing (9,879 vs 4,884) is NOT resolved here; p.22 not in this capture.", "evidence": [{"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 24, "quote": "The cumulative impairment gain of R431 million relates to elevated performance"}]}, {"question_id": "Q-d22e0c2b395a427e", "status": "partial", "answer": "ECL allowance movement on principal books supplied: 598 (30 Sep 25) -> 431 (31 Mar 26), net -167 = acquired-book gain +24 less historical-book loss -191. Driver: payer drop-offs and reduced settlement activity on historical books. Full PBD roll-forward (acquisitions, collections, amortisation) and model-vs-collections split NOT supplied here.", "evidence": [{"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 24, "quote": "Impairment (loss)/gain on principal book portfolios | (241) | 69 | 4 | 1 | (167)"}]}, {"question_id": "Q-e4497d9112cd4e9d", "status": "partial", "answer": "Measurement basis not explicitly labelled, but the cumulative impairment GAIN presentation (R431m) is consistent with a POCI-style acquired-book measurement rather than a conventional ECL reserve. Roll-forward to the R4,489m carrying value NOT supplied here.", "evidence": [{"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 24, "quote": "Balance at 31 March 2026 – Unaudited | 227 | 141 | 51 | 12 | 431"}]}, {"question_id": "Q-f8a0c48e3545479f", "status": "partial", "answer": "ECL allowance movement and qualitative driver supplied (see Q-d22e0c2b395a427e). Principal-vs-agency revenue split and full PBD/RTC amortisation roll-forward NOT supplied here.", "evidence": [{"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 24, "quote": "The reduction in the cumulative impairment gain in the current year relates to payer drop-offs"}]}, {"question_id": "Q-86ab4a63039b4d7e", "status": "partial", "answer": "ECL allowance movement supplied; principal-vs-agent revenue split and PBD/RTC amortisation basis NOT supplied here.", "evidence": [{"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 24, "quote": "Impairment gain on principal book portfolios acquired during the period | 1 | 23 | - | - | 24"}]}], "new_questions": [{"question": "Reconcile the R431m cumulative impairment gain on principal book portfolios (D003.11, p.24) to the p.22 'Financial assets subject to risk' principal-book net carrying value and to the statement of financial position (p.8). Confirm whether the acquired-book +24 gain is a POCI measurement gain (not an ECL reserve movement), and provide gross carrying value plus the split of the acquired-book gain between model/assumption change and collections performance, in Rm, at 31 Mar 2026 vs 30 Sep 2025 and 31 Mar 2025.", "priority": "high", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003.10 pp.21-23 (PBD detail, p.22 table); D003.1 p.8 (SoFP); D003.4 p.13 (Note 1)", "evidence_required": "Gross carrying value, cumulative impairment gain and net carrying value for principal books by segment, Rm, at 31 Mar 2026, 30 Sep 2025 and 31 Mar 2025; reconciliation to SoFP; acquired-book gain driver split (model vs collections); confirmation of POCI vs ECL measurement basis", "closure_condition": "R431m cumulative gain reconciles to the p.22 principal-book net carrying value and SoFP, and the acquired-book gain is identified as POCI measurement gain or ECL movement, or confirmed not disclosed; benign explanations (presentation, POCI measurement) acceptable. Forecast consequence: correct ECL base, amortisation projection and earnings-quality assessment."}]}
```