### 1. Answers to Stored Questions for This Section

- **Q-PILOT-ntu_portfolio**:
- **Status**: `Partially resolved (remainder stays open for D003.3 cash flow / D003.1 statement of financial position)`
- **Answer & evidence**: The two portfolios are now separately reconciled for the period `[D003.4, physical PDF p. 13]`:
  - **Principal book portfolio** (amortised cost, credit-impaired at acquisition, CAEIR interest): opening R3,975m + additions R382m − net cash collections R728m + CAEIR interest R383m − impairment loss R167m = **closing R3,845m**. Arithmetic checks: 3,975 + 382 − 728 + 383 − 167 = 3,845. ✓
  - **Other financial assets** (fair value, no title, no recourse): opening R702m + additions R28m − cash collections R116m + fair value movements R30m = **closing R644m**. Arithmetic checks: 702 + 28 − 116 + 30 = 644. ✓
  - Total purchased book debts R4,489m (R3,845m principal + R644m other) reconciles to the maturity split (R3,178m >12m + R1,311m <12m = R4,489m). ✓
  - **Still open**: the bridge of these carrying movements to the statutory cash flow statement (D003.3) — specifically whether the R728m "net cash collections" (gross R773m less R45m collection costs) and the R116m other-asset collections appear as investing/operating inflows, and whether CAEIR interest (R383m) and impairment (R167m) are non-cash. Also whether the R3,845m pledged principal book ties to the interest-bearing liabilities note (D003.1 / note 2).

### 2. Footnote & Qualification Deep-Dive

- **`*` Pledge footnote** `[D003.4, p. 13]`: R3,845m of purchased book debts (100% of the principal book carrying value; 31 Mar 2025: R3,690m; 30 Sep 2025: R3,975m) is **pledged as security for interest-bearing liabilities and bank overdrafts** for the duration of the agreement. Implication: the entire principal book is encumbered — no unpledged collateral buffer; recovery on these assets is effectively subordinated to secured lenders. Must verify covenant/trigger terms and the funded-debt quantum in note 2 (D003.1) and the funding note.
- **`**` Collections footnote** `[D003.4, p. 13]`: Net collections R728m = gross collections R773m less directly attributable and incremental collection costs R45m (prior: R604m gross / R38m costs; FY25: R1,280m gross / R83m costs). Implication: collection cost ratio ≈ 5.8% of gross collections (H1 FY26) vs 6.3% (H1 FY25) vs 6.5% (FY25) — modest efficiency gain, but costs are netted into "collections," so gross collection performance is understated in the movement line. Verify whether collection costs are also expensed in opex (double-count risk) in the income statement (D003.2).
- **Accounting policy qualification (no footnote marker, but material)** `[D003.4, p. 13]`: Principal book is **credit-impaired (POCI) at acquisition**, measured at amortised cost with a **lifetime ECL loss allowance**; favourable ECL changes are recognised as **impairment gains even where lifetime ECL is below acquisition-date expected losses**. This is a POCI-style gross-up mechanic — impairment "loss" of R167m in H1 is a net charge; the gross-up unwind (CAEIR interest R383m) inflates interest income. Verify the split of the R167m between (a) ECL allowance movement and (b) write-offs/recoveries, and whether any impairment *gain* reversals occurred, in D003.2/D003.5.
- **Other financial assets qualification** `[D003.4, p. 13]`: Measured at **fair value** (fails SPPI — no title, no recourse, titleholder retraction rights, Nutun entitled to a portion of third-party disposal proceeds). Fair value movements R30m (H1 FY26) vs R74m (H1 FY25) vs R114m (FY25) — a sharp deceleration in fair value gains; verify valuation inputs/Level and whether gains are being sustained by model assumption changes (refer note 6.3, not in this capture).

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| N1 | High | D003.3 (cash flows, p.12) | Net cash collections R728m and other-asset collections R116m `[D003.4, p.13]` | Reconcile R728m and R116m to the cash flow statement lines (operating/investing); confirm CAEIR interest R383m and impairment R167m are non-cash | Confirms cash conversion and whether collections are the true cash engine |
| N2 | High | D003.1 (SoFP, p.8) / note 2 | R3,845m principal book pledged for interest-bearing liabilities & overdrafts `[D003.4, p.13]` | Tie pledged amount to secured borrowings; obtain covenant/trigger terms and headroom | Encumbrance and covenant breach risk to funding |
| N3 | High | D003.2 (income statement, p.9–11) | Impairment loss R167m; CAEIR interest R383m `[D003.4, p.13]` | Locate impairment charge and interest income lines; check for impairment *gain* reversals and collection-cost double count | Drives CLR, NIM and risk-adjusted margin |
| N4 | Medium | D003.5 / note 6.3 (fair value) | Other financial assets fair value gains R30m vs R74m prior `[D003.4, p.13]` | Obtain fair value hierarchy, key assumptions, and sensitivity for the R644m book | Tests sustainability of non-interest income |
| N5 | Medium | D003.2 / D003.1 | Additions R382m (principal) vs R857m FY25; R28m other `[D003.4, p.13]` | Confirm purchase spend in cash flow and whether growth is decelerating | Forward purchase-volume and revenue driver |

### 4. Updated Open Questions Ledger


### 5. Baseline Forecast Inputs Captured Here

| Metric (Rm unless stated) | 31 Mar 2026 | 31 Mar 2025 | 30 Sep 2025 |
| --- | --- | --- | --- |
| Principal book portfolio (>12m) | 2,688 | 2,592 | 2,853 |
| Other financial assets (>12m) | 490 | 500 | 546 |
| Principal book portfolio (<12m) | 1,157 | 1,098 | 1,122 |
| Other financial assets (<12m) | 154 | 163 | 156 |
| **Total purchased book debts** | **4,489** | **4,353** | **4,677** |
| Principal book opening | 3,975 | 3,831 | 3,831 |
| Principal additions | 382 | 265 | 857 |
| Principal net cash collections | (728) | (566) | (1,197) |
| Principal CAEIR interest | 383 | 333 | 683 |
| Principal impairment loss | (167) | (173) | (199) |
| Principal book closing | 3,845 | 3,690 | 3,975 |
| Other FA opening | 702 | 672 | 672 |
| Other FA additions | 28 | 7 | 84 |
| Other FA cash collections | (116) | (90) | (168) |
| Other FA fair value movements | 30 | 74 | 114 |
| Other FA closing | 644 | 663 | 702 |
| Gross collections (principal) | 773 | 604 | 1,280 |
| Collection costs | 45 | 38 | 83 |
| Pledged principal book | 3,845 | 3,690 | 3,975 |

### 6. Next Section to Capture
**D003.3 (Condensed consolidated statement of cash flows, p. 12)** — resolves N1 and N5 (cash-flow bridge of collections, CAEIR interest, impairment, additions). Then **D003.1 (SoFP, p. 8) / note 2** for N2 (pledge/covenant tie-out).