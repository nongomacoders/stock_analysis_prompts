### 1. Answers to Stored Questions for This Section

- **Q-PILOT-ntu_shared_page**:
- **Status**: `Partially resolved (remainder stays open for D003.12 continuation / D003.11 reconciliation)`
- **Answer & evidence**: The capture establishes the trade-receivable ECL measurement basis as a **maturity-bucketed expected-loss-rate matrix** (Current / 1–30 / 31–60 / 61–90 / 90+ days overdue), with loss allowance applied per bucket `[D003.12, physical PDF p. 25]`. Hard figures at 31 March 2026 (unaudited): gross carrying amount R374m, loss allowance R(5)m, net carrying R369m, total expected loss rate 1.34%; the entire allowance sits in the 90+ days overdue bucket (100.00% loss rate on R5m) `[D003.12, physical PDF p. 25]`. Comparatives: 31 March 2025 gross R419m / allowance R(6)m / net R413m / 1.43%; 30 September 2025 (audited) gross R364m / allowance R(10)m / net R354m / 2.75% `[D003.12, physical PDF p. 25]`. **Still open**: (i) the note is a shared-page continuation — the trade-receivable ECL reconciliation and any staging/overlay narrative may continue on p. 26; (ii) the footnote states credit risk is managed by reference to past default experience and forward-looking conditions, but **no macro overlay, scenario weighting, or SICR threshold is disclosed here**; (iii) the 0.00% loss rates on Current and 1–90 day buckets at both 31 March 2026 and 31 March 2025 are inconsistent with the 30 September 2025 audited rates (0.06% / 0.19% / 6.67%) and require verification — this is a measurement-basis anomaly, not a resolved policy conclusion.

### 2. Footnote & Qualification Deep-Dive

- **Footnote `*` (p. 25)**: States ECL on trade receivables is shown **per maturity of trade receivables**; "no separate classes of trade receivables have been identified"; receivables arise from customer contracts across industries/geographies; credit risk managed by reference to **past default experience, debtor financial position, debtor-specific factors, and current/forecast direction of conditions**; disclosure **first presented in the FY2025 AFS** to "enhance overall presentation." Implication: this is a **new disclosure, not a new policy** — but the forward-looking/scenario machinery described in the footnote is **not quantified anywhere in this capture** (no base/upturn/downturn weightings, no overlay amount). Must be verified against D003.9 (Credit risk management) and D003.11 (ECL reconciliation).
- **Footnote `**` (p. 25)**: 31 March 2025 comparative **presented for the first time**. Implication: the March 2025 column is a **restated/first-time comparative**, so any trend read across 31-Mar-25 → 30-Sep-25 → 31-Mar-26 mixes a newly constructed comparative with audited and unaudited figures — treat the 1.43% → 2.75% → 1.34% path with caution.
- **Unmarked anomaly (no footnote)**: The **0.00% expected loss rate on Current, 1–30, and 31–60 day buckets at both 31 March 2026 and 31 March 2025**, versus 0.06% / 0.19% / 6.67% at 30 September 2025, is unexplained. Either the interim measurement applies a **zero-loss assumption to non-90+ buckets** (a methodology change vs the audited year-end) or the interim table is incomplete. This is a **material measurement-basis question** and is not covered by any printed footnote.
- **Arithmetic check**: 31-Mar-26: 339+25+5+5 = 374 ✓; allowance (5) all in 90+ ✓; net 369 ✓; 5/374 = 1.34% ✓. 31-Mar-25: 345+61+6+7 = 419 ✓; (6)/419 = 1.43% ✓. 30-Sep-25: 286+52+15+11 = 364 ✓; (10)/364 = 2.75% ✓. Bucket arithmetic reconciles; the **rate anomaly is a policy/measurement issue, not an addition error**.
- **Currency risk (6.2)**: USD/GBP receivables realised in **60 days**; FX contracts entered to hedge Nutun International USD/GBP receipts. Relevant to trade-receivable ECL only insofar as FX moves affect recoverable Rand value — no ECL interaction quantified.

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| N1 | High | D003.12 continuation (p. 26) | Shared-page note may continue; trade-receivable ECL reconciliation not fully shown `[D003.12, p. 25]` | Check p. 26 for continuation of the trade-receivable ECL table, any movement reconciliation (opening allowance → write-offs → recoveries → closing), and any staging/overlay note | Needed to bridge gross write-offs/recoveries and confirm whether the R5m allowance is a full-period movement or a point-in-time balance |
| N2 | High | D003.9 Credit risk management (p. 20) | Footnote `*` cites forward-looking conditions and debtor-specific factors but no scenario weightings/overlay quantified `[D003.12, p. 25]` | Extract the stated IFRS 9 methodology: SICR definition, DPD backstops, macro scenario weightings (base/upturn/downturn), and any management overlay amount | Determines whether the 1.34% total loss rate is comparable across periods and whether overlays are being released to smooth P&L |
| N3 | High | D003.11 ECL reconciliation (p. 24) | 0.00% loss rates on Current/1–30/31–60 buckets at 31-Mar-26 and 31-Mar-25 vs 0.06%/0.19%/6.67% at 30-Sep-25 `[D003.12, p. 25]` | Reconcile the trade-receivable allowance movement and confirm whether interim periods apply a zero-loss assumption to non-90+ buckets or whether the table is incomplete | A methodology change between audited year-end and interim would distort period-on-period credit loss ratio and forecast |
| N4 | Medium | D003.10 Purchased book debts (pp. 21–23) | Trade receivables (R374m gross) sit alongside purchased book debt portfolios; footnote says no separate classes identified `[D003.12, p. 25]` | Confirm whether trade receivables are separate from purchased book debts and whether any purchased-book-debt ECL is double-counted or omitted from this table | Avoids double-counting credit losses across the two receivable populations in the forecast |
| N5 | Medium | D003.2 Income statement (pp. 9–11) | No impairment charge attributable to trade receivables is shown in this capture `[D003.12, p. 25]` | Locate the P&L impairment line and split trade-receivable ECL movement from purchased-book-debt ECL movement | Needed to compute a clean credit loss ratio and risk-adjusted margin |
| N6 | Low | D003.12 / D003.9 | Footnote `**`: 31-Mar-25 comparative presented for the first time `[D003.12, p. 25]` | Confirm whether the 31-Mar-25 comparative was restated or newly constructed, and whether it is consistent with the FY2025 audited 30-Sep-25 figures | Trend reliability for vintage/roll-rate analysis |

### 4. Updated Open Questions Ledger



### 5. Baseline Forecast Inputs Captured Here

| Metric | 31-Mar-2026 (Unaudited) | 31-Mar-2025 (Unaudited, first-time) | 30-Sep-2025 (Audited) |
| --- | --- | --- | --- |
| Trade receivables gross carrying (Rm) | 374 | 419 | 364 |
| — Current | 339 | 345 | 286 |
| — 1–30 days overdue | 25 | 61 | 52 |
| — 31–60 days overdue | 5 | 6 | 15 |
| — 61–90 days overdue | 0 (implied) | 0 (implied) | 0 (implied) |
| — 90+ days overdue | 5 | 7 | 11 |
| Loss allowance (Rm) | (5) | (6) | (10) |
| Net carrying amount (Rm) | 369 | 413 | 354 |
| Total expected loss rate | 1.34% | 1.43% | 2.75% |
| 90+ loss rate | 100.00% | 85.71% | 81.82% |
| Current / 1–30 / 31–60 loss rates | 0.00% / 0.00% / 0.00% | 0.00% / 0.00% / 0.00% | 0.06% / 0.19% / 6.67% |
| FX rates (closing, 31-Mar-26): USD 17.2 / EUR 19.7 / GBP 22.7 / AUD 11.8 | | | |

### 6. Next Section to Capture

**D003.11 — Reconciliation of expected credit loss allowance on principal book portfolios (p. 24)**, followed by the **D003.12 continuation on p. 26**. D003.11 will resolve **N3** (rate anomaly / allowance movement) and inform **N2** (methodology/overlay); p. 26 will resolve **N1** (note continuation and movement reconciliation).