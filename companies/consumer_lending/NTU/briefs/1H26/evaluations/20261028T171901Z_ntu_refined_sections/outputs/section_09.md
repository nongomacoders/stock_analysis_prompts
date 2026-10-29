## Section 1 — Key facts and figures (D003.4, physical p.13)

**Measurement basis (explicit):**
- **Principal book portfolios** — purchased credit-impaired (POCI) consumer debt at deep discount; carried at **amortised cost on a portfolio basis**, with cumulative changes in lifetime ECL since acquisition as a loss allowance; favourable ECL changes recognised as impairment gains. Interest accreted at the **credit-adjusted effective interest rate (CAEIR)**.
- **Other financial assets** — purchased book debt where Nutun lacks title; no recourse to banks/credit providers; titleholder may retract accounts; cash flows not SPPI → **fair value** (note 6.3).

**Carrying values (Rm):**

| | 31 Mar 2026 (U) | 31 Mar 2025 (U) | 30 Sep 2025 (A) |
|---|---|---|---|
| Principal book — >12m | 2,688 | 2,592 | 2,853 |
| Other fin. assets — >12m | 490 | 500 | 546 |
| Principal book — <12m | 1,157 | 1,098 | 1,122 |
| Other fin. assets — <12m | 154 | 163 | 156 |
| **Total PBD** | **4,489** | **4,353** | **4,677** |

**Principal book roll-forward (Rm):** opening 3,975 + additions 382 − net collections 728 + CAEIR interest 383 − impairment 167 = **3,845** (Mar-26). Mar-25: 3,831 + 265 − 566 + 333 − 173 = **3,690**. Sep-25 FY: 3,831 + 857 − 1,197 + 683 − 199 = **3,975**. All three foot.

**Other financial assets roll-forward (Rm):** Mar-26: 702 + 28 − 116 + FV gain 30 = **644**. Mar-25: 672 + 7 − 90 + 74 = **663**. Sep-25: 672 + 84 − 168 + 114 = **702**. All foot.

**Reconciliation to total:** 3,845 + 644 = **4,489** ✓ (Mar-26); 3,690 + 663 = 4,353 ✓; 3,975 + 702 = 4,677 ✓.

**Pledge:** R3,845m principal book pledged as security for interest-bearing liabilities and overdrafts (note 2) — i.e. essentially the entire principal book.

**Collections footnote:** net collections 728 = gross 773 − collection costs 45 (Mar-26); 566 = 604 − 38 (Mar-25); 1,197 = 1,280 − 83 (Sep-25).

## Section 2 — Footnotes, qualifications and reconciliations

- **POCI treatment confirmed.** The note explicitly frames principal book as credit-impaired at acquisition with lifetime-ECL-since-acquisition allowance — so ordinary Stage 1/2 SICR migration is not the right lens; the relevant credit metric is change in lifetime expected losses vs acquisition assumptions. Impairment loss of 167 (Mar-26) vs 173 (Mar-25) is a net charge; the note permits favourable re-estimates to be booked as gains, so the gross direction is not disclosed.
- **CAEIR accretion is large relative to cash:** interest 383 vs net collections 728 — accretion ≈ 53% of collections, so carrying value is highly sensitive to the CAEIR assumption and to collection-timing assumptions embedded in it.
- **Additions slowed:** 382 (H1-26) vs 265 (H1-25) vs 857 (full FY25) — H1-26 run-rate below FY25; relevant to volume vs assumption split of amortisation (Q-c3d790bf…).
- **Other financial assets FV gain** fell to 30 (H1-26) from 74 (H1-25) and 114 (FY25) — a material swing in a fair-valued, non-recourse book; driver not disclosed here.
- **Scope note:** the note does not itself state the R4,489m ties to the statement of financial position line (p.8 not supplied); the internal roll-forward arithmetic does tie. Treat SoFP tie-out as Pending: D003.1 (p.8).
- **Units:** all Rm; no per-unit or scaling conflict found; arithmetic consistent.

## Section 3 — Questions answered and next evidence

- **Q-e4497d9112cd4e9d** — *partial → resolved on basis; roll-forward now supplied and foots to 4,489.* Measurement basis (amortised cost POCI + FV other) and full roll-forward disclosed. Residual: SoFP tie-out (p.8) not in capture.
- **Q-86ab4a63039b4d7e** — *partial.* PBD/RTC roll-forward and basis now disclosed; principal-vs-agency **revenue** split still not in this note → Pending: D003 segmental note 7.
- **Q-c3d790bf20794c50** — *partial.* Basis and carrying value answered; volume-vs-macro split of amortisation **not** disclosed here → Pending: D003 segmental/CFO commentary.
- **Q-e0ca727b62be46df, Q-31753fb252ee4ed2, Q-f8db08b395c448a9, Q-23af9329edce40eb, Q-7ccb4721205d4f99, Q-b18d8ce6d4804a50, Q-8612694a3a674266, Q-b6d6eda13d854fdf, Q-5973eb62939a4c48** — not addressed by this note; remain open/partial.

**New material questions (see JSON):** (i) gross vs net impairment direction and recovery-assumption sensitivity of the POCI book; (ii) driver of the FV gain fall in other financial assets and note 6.3 basis; (iii) SoFP tie-out and pledged-asset covenant linkage (note 2).

**Next evidence:** D003.1 (p.8) SoFP tie-out; D003 note 6.3 (FV basis); D003 note 2 (pledge/funding); D003 segmental note 7 (revenue split, amortisation drivers).

## Section 4 — Updated Open Questions Ledger

```json
{"ledger_version": 1, "updates": [
  {"question_id": "Q-e4497d9112cd4e9d", "status": "resolved", "answer": "Principal book portfolios are POCI assets measured at amortised cost on a portfolio basis with cumulative lifetime-ECL-since-acquisition allowance and CAEIR interest accretion; other financial assets (no title, non-SPPI) are at fair value. Roll-forward Mar-26: 3,975 + 382 additions - 728 net collections + 383 CAEIR - 167 impairment = 3,845; other financial assets 702 + 28 - 116 + 30 FV = 644; total 4,489, tying to the note total (SoFP p.8 tie-out pending).", "evidence": [
    {"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 13, "quote": "Principal book portfolios are reflected at amortised cost on a portfolio basis."},
    {"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 13, "quote": "Total purchased book debts | 4 489 |  | 4 353 | 4 677 |"},
    {"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 13, "quote": "Balance at the end of the period | 3 845 |  | 3 690 | 3 975 |"}
  ]},
  {"question_id": "Q-86ab4a63039b4d7e", "status": "partial", "answer": "PBD/RTC roll-forward and measurement basis now disclosed (principal book amortised cost POCI; other financial assets FV). Principal-vs-agency revenue split still not in this note.", "evidence": [
    {"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 13, "quote": "Accordingly, these purchased book debts are measured on a fair value basis. Refer to note 6.3."}
  ]},
  {"question_id": "Q-c3d790bf20794c50", "status": "partial", "answer": "Amortisation basis and remaining carrying value answered: CAEIR accretion 383 (H1-26) vs 333 (H1-25); closing principal book 3,845. Volume-vs-macro split of amortisation not disclosed in this note.", "evidence": [
    {"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 13, "quote": "Interest calculated using the credit-adjusted effective interest rate (CAEIR) | 383 |  | 333 | 683 |"}
  ]}
], "new_questions": [
  {"question": "What is the gross vs net direction of the POCI impairment charge (R167m H1-26; R173m H1-25) — i.e. gross favourable re-estimates vs gross adverse changes in lifetime ECL since acquisition — and what recovery/collection-timing assumptions drive it? Provide the split and any sensitivity, Rm, H1-26 vs H1-25.", "priority": "high", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003.4 note 1 / D003 credit-risk note", "evidence_required": "Gross favourable and adverse lifetime-ECL movements, recovery-rate and collection-timing assumptions, sensitivity in Rm, H1-26 vs H1-25", "closure_condition": "Gross direction and key assumptions disclosed, or confirmed not disclosed; benign explanation (net presentation) acceptable. Forecast consequence: POCI impairment projection and CAEIR sensitivity."},
  {"question": "What drove the fall in other financial assets fair-value gain to R30m (H1-26) from R74m (H1-25) and R114m (FY25), and what is the note 6.3 fair-value basis (level, inputs, retraction risk)?", "priority": "medium", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003 note 6.3 / D003.4 note 1.2", "evidence_required": "FV movement composition, valuation level/inputs, retraction/recourse commentary, Rm, across the three dates", "closure_condition": "Driver and valuation basis disclosed, or confirmed not disclosed; forecast consequence: FV earnings volatility."},
  {"question": "Does the R4,489m total purchased book debts tie to the statement of financial position line at 31 Mar 2026, and how does the R3,845m pledged principal book interact with funding covenants (note 2)?", "priority": "medium", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003.1 statement of financial position (p.8) / D003 note 2", "evidence_required": "SoFP PBD line at 31 Mar 2026, 31 Mar 2025, 30 Sep 2025; pledge/covenant terms and headroom", "closure_condition": "SoFP tie-out shown and pledge/covenant linkage disclosed, or confirmed not disclosed; forecast consequence: asset encumbrance and refinancing risk."}
]}
```