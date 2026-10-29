> APPLICATION QUALIFICATION: DeepSeek ledger updates failed evidence validation. No existing question was resolved by this response. All prior questions remain open; any resolution claim in the narrative is unverified. Only valid new questions were retained.

### 1. Answers to Stored Questions for This Section

**Q-3df04995ff2f4c6a [high] — Extract headline financial metrics and confirm page offset**
- **Status**: `Partially resolved (remainder stays open for D002/D003 notes)`
- **Answer & evidence**: Page offset confirmed: printed footer "6" on physical p. 8, "7" on p. 9, "8" on p. 10, "9" on p. 11, "10" on p. 12, "11" on p. 13, "12" on p. 14, "13" on p. 15 → printed = physical − 2. Statement-level metrics captured: total assets R6,444m (31 Mar 2026) vs R6,661m (31 Mar 2025) vs R6,604m (30 Sep 2025); total equity R1,329m vs R1,551m vs R1,396m; loss for the period R(63)m vs R(64)m vs R(238)m; basic LPS total operations (8.1)c vs (8.2)c vs (30.3)c `[D003, physical PDF pp. 8–9]`. No HEPS, DPS, CLR%, NIM% or management guidance/targets appear in this capture — those remain open for D002/D003 notes.

**Q-995d98c7cabc40ba [high] — Statement lines, advances, ECL allowance, Stage 1/2/3 split**
- **Status**: `Partially resolved (Stage 1/2/3 split and ECL allowance remain open)`
- **Answer & evidence**: Statement lines captured. Purchased book debts R4,489m (31 Mar 2026) vs R4,353m (31 Mar 2025) vs R4,677m (30 Sep 2025) `[D003, physical PDF p. 8]`. Principal book portfolio gross reconciliation: opening R3,975m + additions R382m − net cash collections R728m + CAEIR interest R383m − impairment loss R167m = closing R3,845m `[D003, physical PDF p. 13]`. **No Stage 1/2/3 ECL staging table, no separate ECL allowance balance, and no SICR disclosure appear in this capture** — the impairment loss of R167m is a P&L charge only; the closing carrying value is stated net. Stage split and allowance balance remain open for later D003 notes (pp. 16–37).

**Q-64b704d06ed84c90 [medium] — Cash flow: write-offs, recoveries, debt raised/repaid, dividends**
- **Status**: `Partially resolved (write-offs/recoveries not separately disclosed)`
- **Answer & evidence**: Cash flow statement captured `[D003, physical PDF p. 12]`. Debt raised R1,145m; debt settled R(842)m; overdraft draw-down R3,178m / settlement R(3,269)m; lease repayments R(30)m; treasury shares R(4)m. **No dividend paid line** (consistent with nil dividend). **No gross write-off or bad-debt recovery lines** — the cash flow presents purchased book debt collections net (R182m decrease in operating assets). Net bad debt charge reconciliation (write-offs + ECL movement − recoveries) is therefore **not testable from this capture**; remains open for later notes.

**Q-336536b6077249e3 [medium] — IFRS 9 ECL staging, SICR, macro overlay, write-off policy, covenants**
- **Status**: `Partially resolved (policy narrative captured; staging/SICR/covenants remain open)`
- **Answer & evidence**: Note 1 `[D003, physical PDF p. 13]` confirms principal book portfolios are **purchased credit-impaired financial assets at initial recognition**, held at amortised cost on a portfolio basis, with cumulative changes in **lifetime ECL** since acquisition recognised as an impairment gain/loss. Favourable ECL changes (collections outperforming acquisition expectations) are recognised as an impairment **gain** even where lifetime ECL is below acquisition-date expected losses — a P&L-smoothing mechanism to scrutinise. Other financial assets (no title; non-SPPI) are at **fair value** (note 6.3 referenced but not in capture). **No SICR thresholds, DPD staging, macro scenario weightings, write-off triggers, modification/re-aging rules, or covenant terms appear in this capture** — remain open.

**Q-007f8f020e154296, Q-e741a412cfd44a34, Q-b63cf1b01b6d4cf8, Q-b3d2bdde10394bac, Q-fec447426706441e, Q-7acc435c1ae94e77, Q-c06d7a5336224c7e, Q-e8e8f8f7354146ea, Q-174a38f8f4c04abc, Q-aea94945233b418a, Q-59b88716280048c3, Q-ebf661d7f2e740cd, Q-0b9b00a6c7da4496, Q-5a1c41b2ef654626**
- **Status**: `Open` — the underlying question text for these IDs was not supplied in this prompt (only "Pending: D003" status lines). They cannot be answered without their question wording; carried forward unchanged in Section 4.

**Q-add37e0058a74df2 [low] — Audit/review status and APM add-backs**
- **Status**: `Partially resolved (assurance status confirmed; APM add-backs remain open)`
- **Answer & evidence**: Every primary statement is labelled **"Unaudited"** for 31 Mar 2026 and 31 Mar 2025, with 30 Sep 2025 labelled **"Audited"** `[D003, physical PDF pp. 8–12]`. No core continuing earnings reconciliation or "accelerated/normal operations" add-back table appears in this capture — remains open.

---

### 2. Footnote & Qualification Deep-Dive

- **Cash footnote (*), p. 12** `[D003, physical PDF p. 12]`: "Cash and cash equivalents presented include R1 million (31 March 2025: R2 million; 30 September 2025: R1 million) of cash included in assets held for sale." → Closing cash R113m includes R1m held-for-sale cash; clean-up adjustment of R1m needed for continuing-operations liquidity. Minor but confirms held-for-sale perimeter still open.

- **Note 1 pledge footnote (*), p. 13** `[D003, physical PDF p. 13]`: "Purchased book debts of R3,845 million … have been pledged as security for the interest-bearing liabilities and bank overdrafts per the pledge agreement … for the duration of the agreement." → **100% of the principal book portfolio (R3,845m) is encumbered.** This is a critical funding-structure finding: the entire purchased book debt asset base secures R4,016m of interest-bearing liabilities plus overdrafts. Asset encumbrance is effectively total; there is no unpledged collateral buffer. Must be cross-checked against covenant/security-cover terms in the funding note (not in capture).

- **Note 1 net collections footnote (**), p. 13** `[D003, physical PDF p. 13]`: "Included in net collections are gross collections of R773 million (31 March 2025: R604 million; 30 September 2025: R1 280 million) and directly attributable and incremental collection costs of R45 million (31 March 2025: R38 million; 30 September 2025: R83 million)." → Gross collections R773m − collection costs R45m = R728m net, reconciling to the movement table. **Collection cost ratio = 5.8% of gross collections** (H1 2025: 6.3%; FY2025: 6.5%) — modest efficiency improvement. Note the H1 2026 gross collections of R773m vs FY2025 R1,280m implies a **run-rate deceleration** (H1 annualised ≈ R1,546m would be growth, but H2 FY2025 alone was R676m — so H1 2026 R773m is +14% HoH; needs vintage/seasoning context). Also note: gross collections R773m vs net cash collections R728m — the R45m cost is deducted inside "net cash collections," meaning the cash flow statement's R182m "decrease in purchased book debts" is already net of collection costs.

- **Note 2 footnote (*), p. 14** `[D003, physical PDF p. 14]`: "Comparative disclosure for 31 March 2025 has been presented for the first time to enhance the overall presentation of the financial statements." → **The 31 Mar 2025 comparative interest-bearing liability maturity/type breakdown is a new disclosure, not previously presented.** This is a presentation change, not a restatement, but it means prior-period comparability for funding maturity analysis is limited to one period. Flag for consistency check in FY2026.

- **Note 2.1 footnote (*), p. 15** `[D003, physical PDF p. 15]`: Pledge footnote repeated — "Purchased book debts, trade and other receivables and cash and cash equivalents have been pledged as security…" → Confirms the encumbrance extends beyond book debts to receivables and cash. Combined with the p. 13 footnote, essentially the entire current-asset base is pledged.

- **Note 2.1 footnote (**), p. 15** `[D003, physical PDF p. 15]`: Same "comparative presented for the first time" qualification repeated for the loan-type/maturity table. → The detailed facility-level maturity and interest-rate table (JIBAR + spreads, Prime − 0.25% to 0.35%) is **new disclosure**; useful for interest-rate sensitivity but unverifiable against prior periods.

- **Note 1 policy narrative (unfootnoted but commentary-heavy), p. 13** `[D003, physical PDF p. 13]`: "Favourable changes in lifetime expected credit losses (where collections on portfolios are expected to outperform the collections expected when the portfolios were acquired) are recognised as an impairment gain even if the lifetime expected credit losses are less than the value of expected credit losses that were included in the estimated cash flows when acquired." → This is a **P&L gain-recognition mechanism on purchased credit-impaired books**. It means impairment loss of R167m in H1 2026 is a *net* figure that could be masking gross deterioration offset by favourable re-estimates. Must be decomposed in later notes (gross ECL charge vs favourable re-estimate gain). Also: "Other financial assets … Nutun has no recourse to the banks or credit providers … titleholder may retract some of the underlying accounts … measured on a fair value basis. Refer to note 6.3." → **Note 6.3 is referenced but not in this capture** — fair value methodology, retraction risk, and Level 3 inputs must be verified.

- **Missing footnote check**: No footnote markers in this capture lack a corresponding definition within the supplied pages. However, **note 6.3 (fair value of other financial assets) is cross-referenced but not supplied** — flagged as a verification question.

---

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| N1 | High | D003 (pp. 16–37 notes) | Principal book portfolio closing R3,845m is stated **net**; impairment loss R167m is P&L only; no ECL allowance balance or Stage 1/2/3 split disclosed `[D003, p. 13]` | Locate ECL/impairment note: gross carrying amount, cumulative ECL allowance, Stage 1/2/3 (or purchased-credit-impaired) split, coverage ratios | Needed to compute coverage %, CLR on gross advances, and assess provisioning adequacy |
| N2 | High | D003 (pp. 16–37 notes) | Policy allows **favourable ECL re-estimates recognised as impairment gains** even below acquisition-date expected losses `[D003, p. 13]` | Find impairment note decomposing R167m into gross ECL charge vs favourable re-estimate gain; check comparative H1 2025 R173m and FY2025 R199m on same basis | If gains are recurring, underlying credit deterioration is understated; affects CLR forecast |
| N3 | High | D003 (pp. 16–37 notes) | **100% of principal book portfolio (R3,845m) pledged** as security; receivables and cash also pledged `[D003, pp. 13, 15]` | Locate funding/borrowings note: security-cover ratio, LTV, borrowing-base covenant, minimum collateral thresholds, headroom | Total encumbrance = no unpledged buffer; covenant breach risk on collateral value decline |
| N4 | High | D003 (pp. 16–37 notes) | Interest-bearing liabilities R4,016m; **R1,396m payable within 12 months**; undrawn overdraft facilities only R475m `[D003, p. 14]` | Find maturity profile by facility, refinancing plan, covenant ratios (interest cover, DSCR), and going-concern statement | Refinancing wall + thin undrawn liquidity = liquidity risk to forecast |
| N5 | High | D003 (pp. 16–37 notes) | Note 6.3 referenced for **fair value of other financial assets (R644m)** but not supplied; retraction risk disclosed `[D003, p. 13]` | Locate note 6.3: fair value hierarchy level, valuation inputs, retraction/recourse terms, sensitivity | R644m (14% of book debts) at fair value with retraction risk — valuation and earnings volatility |
| N6 | Medium | D003 (pp. 16–37 notes) | Gross collections R773m vs net R728m; collection cost R45m (5.8%); H1 2026 vs H2 FY2025 (R676m implied) `[D003, p. 13]` | Find vintage/seasoning or ERC note: collection curve assumptions, ERC balance, actual vs expected collections | Tests whether collection performance is genuine or acquisition-driven; drives ERC amortisation forecast |
| N7 | Medium | D003 (pp. 16–37 notes) | Additions R382m (H1 2026) vs R265m (H1 2025) vs R857m (FY2025) — **portfolio acquisition pace decelerating HoH** `[D003, p. 13]` | Find business-combination/portfolio-acquisition note: purchase price, acquired ERC, expected collections, any contingent consideration | Acquisition-driven growth is slowing; organic collection run-off becomes the growth driver |
| N8 | Medium | D003 (pp. 16–37 notes) | Other financial assets: additions R28m, collections R116m, **fair value gain R30m** (H1 2025: R74m; FY2025: R114m) `[D003, p. 13]` | Find note 6.3 / fair value note: drivers of FV gain, whether recurring, Level 3 assumptions | FV gains R30m are 48% of the R63m loss — material to earnings quality |
| N9 | Medium | D003 (pp. 16–37 notes) | Equity accounted loss R(1)m vs R(43)m (H1 2025) vs R(48)m (FY2025); equity accounted investments R87m `[D003, pp. 8–9]` | Find associate note: TC Global Finance carrying value, share of loss, impairment | Sharp swing to near-nil loss needs explanation; residual impairment risk |
| N10 | Medium | D003 (pp. 16–37 notes) | Discontinued operations: **nil** H1 2026 vs +R58m (H1 2025) vs R(125)m (FY2025); proceeds on disposal R398m in H1 2025 `[D003, pp. 9, 12]` | Find discontinued-operations note: what was disposed, any residual liabilities/indemnities, held-for-sale assets R4m/liabilities R6m | Confirms disposal complete; check for residual exposures/warranties |
| N11 | Medium | D003 (pp. 16–37 notes) | Tax: **income tax credit R29m** on loss before tax R(92)m — effective tax rate −31.5% `[D003, p. 9]` | Find tax note: deferred tax asset recognition (R173m), basis for credit on losses, recoverability | A tax credit on a loss is an earnings-quality flag; DTA recoverability depends on forecast profits |
| N12 | Medium | D003 (pp. 16–37 notes) | Operating costs R445m vs R560m (H1 2025) — **−20.5%**; cost of revenue R385m vs R352m (+9.4%) `[D003, p. 9]` | Find opex note: breakdown, one-off items, staff costs, whether cost cut is sustainable | Cost base trajectory drives breakeven forecast |
| N13 | Low | D003 (pp. 16–37 notes) | Revenue R711m vs R745m (−4.6%); gross profit from services R326m vs R393m (−17%) `[D003, p. 9]` | Find revenue disaggregation note: SA vs International, agency fees, DTI incentives | Revenue mix and DTI contingency (carried from D002) |
| N14 | Low | D003 (pp. 16–37 notes) | Treasury shares acquired 4m shares for R4m; shares in issue down to 780m `[D003, p. 11]` | Find EPS note: weighted average shares, dilution from conditional share plans | EPS denominator for forecast |
| N15 | Low | D003 (pp. 16–37 notes) | Note 2.1: **new disclosure** of facility-level rates (JIBAR + 2.8%–5.2%; Prime − 0.25% to 0.35%) and maturities to 2032 `[D003, p. 15]` | Find interest-rate risk/sensitivity note: fixed vs floating split, hedge accounting | Interest expense forecast sensitivity to JIBAR/Prime |

---

### 4. Updated Open Questions Ledger
```json
{"ledger_version": 1, "updates": [], "new_questions": [{"question": "Locate the ECL/impairment note for purchased book debts: capture gross carrying amount, cumulative ECL allowance, Stage 1/2/3 (or purchased-credit-impaired) split, and coverage ratios for 31 Mar 2026 vs 31 Mar 2025 vs 30 Sep 2025, in ZAR millions.", "priority": "high", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003", "evidence_required": "ECL/impairment note: gross carrying amount, cumulative ECL allowance, stage split, coverage ratios, with comparatives and units.", "closure_condition": "Gross advances, allowance and stage split captured; implied coverage % reconciled; any discrepancy flagged; benign explanations noted."}, {"question": "Decompose the R167m impairment loss on principal book portfolios into gross ECL charge vs favourable ECL re-estimate gain, and compare H1 2025 R173m and FY2025 R199m on the same basis.", "priority": "high", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003", "evidence_required": "Impairment note: gross ECL charge, favourable re-estimate gain, net impairment loss, with comparatives.", "closure_condition": "Components quantified; recurring vs one-off classification supported; forecast CLR consequence stated."}, {"question": "Capture funding/borrowings note: security-cover ratio, LTV, borrowing-base covenant, minimum collateral thresholds and headroom, given 100% of principal book portfolio (R3,845m) and receivables/cash are pledged.", "priority": "high", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003", "evidence_required": "Borrowings note: covenant terms, security-cover/LTV ratios, headroom, collateral values, with page references.", "closure_condition": "Covenant ratios and headroom captured; breach risk assessed; forecast consequence stated."}, {"question": "Capture maturity profile by facility, refinancing plan, covenant ratios (interest cover, DSCR) and going-concern statement, given R1,396m payable within 12 months and only R475m undrawn overdraft facilities.", "priority": "high", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003", "evidence_required": "Funding note and going-concern statement: facility maturities, refinancing arrangements, covenant ratios, liquidity reserves.", "closure_condition": "Maturity wall and refinancing plan captured; liquidity risk assessed; forecast consequence stated."}, {"question": "Locate note 6.3 on fair value of other financial assets (R644m): fair value hierarchy level, valuation inputs, retraction/recourse terms and sensitivity.", "priority": "high", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003", "evidence_required": "Note 6.3: fair value hierarchy, valuation inputs, retraction terms, sensitivity analysis.", "closure_condition": "Methodology quoted; valuation and earnings volatility assessed; forecast consequence stated."}, {"question": "Capture vintage/seasoning or ERC note: collection curve assumptions, ERC balance, actual vs expected collections, given gross collections R773m vs net R728m and collection cost R45m (5.8%).", "priority": "medium", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003", "evidence_required": "ERC/vintage note: ERC balance, collection curve assumptions, actual vs expected collections, sensitivity.", "closure_condition": "ERC methodology quoted; actual collections reconciled to ERC run-off; under-run quantified; forecast consequence stated."}, {"question": "Capture portfolio-acquisition note: purchase price, acquired ERC, expected collections and contingent consideration for additions of R382m (H1 2026) vs R265m (H1 2025) vs R857m (FY2025).", "priority": "medium", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003", "evidence_required": "Business-combination/portfolio-acquisition note: purchase price, acquired ERC, expected collections, contingent consideration.", "closure_condition": "Acquisition economics captured; organic vs acquired growth separated; forecast consequence stated."}, {"question": "Capture drivers of the R30m fair value gain on other financial assets (H1 2025 R74m; FY2025 R114m) and assess recurrence.", "priority": "medium", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003", "evidence_required": "Fair value note: drivers of FV gain, Level 3 assumptions, recurrence assessment.", "closure_condition": "FV gain drivers quantified; recurring vs one-off classification supported; forecast consequence stated."}, {"question": "Capture associate note: TC Global Finance carrying value, share of loss (R1m H1 2026 vs R43m H1 2025 vs R48m FY2025) and any residual impairment.", "priority": "medium", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003", "evidence_required": "Associate note: carrying value, share of loss, impairment history, residual exposure.", "closure_condition": "Carrying value and impairment risk captured; forecast consequence stated."}, {"question": "Capture discontinued-operations note: what was disposed (R398m proceeds H1 2025), residual liabilities/indemnities, and held-for-sale assets R4m/liabilities R6m.", "priority": "medium", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003", "evidence_required": "Discontinued-operations note: disposal detail, residual liabilities, indemnities, held-for-sale balances.", "closure_condition": "Disposal complete and residual exposures confirmed or confirmed absent; forecast consequence stated."}, {"question": "Capture tax note: basis for R29m income tax credit on R(92)m loss before tax (effective rate -31.5%), deferred tax asset R173m recognition and recoverability.", "priority": "medium", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003", "evidence_required": "Tax note: current/deferred tax split, DTA recognition basis, recoverability assumptions, comparatives.", "closure_condition": "Tax credit basis captured; DTA recoverability assessed; forecast consequence stated."}, {"question": "Capture operating cost note: breakdown of R445m (vs R560m H1 2025, -20.5%) and cost of revenue R385m (vs R352m, +9.4%), identifying one-off items and sustainability of cost reduction.", "priority": "medium", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003", "evidence_required": "Opex note: breakdown, one-off items, staff costs, cost-of-revenue composition, comparatives.", "closure_condition": "Cost base trajectory captured; one-off vs recurring classified; forecast consequence stated."}, {"question": "Capture revenue disaggregation note: SA vs International split, agency fees, DTI incentive contribution, given revenue R711m vs R745m (-4.6%) and gross profit from services R326m vs R393m (-17%).", "priority": "low", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003", "evidence_required": "Revenue disaggregation note: segment split, agency fees, DTI incentives, comparatives.", "closure_condition": "Revenue mix captured; DTI contingency quantified; forecast consequence stated."}, {"question": "Capture EPS note: weighted average shares, dilution from conditional share plans, given treasury shares acquired (4m for R4m) and shares in issue 780m.", "priority": "low", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003", "evidence_required": "EPS note: weighted average shares, dilution, conditional share plan detail.", "closure_condition": "EPS denominator captured; dilution assessed; forecast consequence stated."}, {"question": "Capture interest-rate risk/sensitivity note: fixed vs floating split and hedge accounting, given new facility-level disclosure of JIBAR + 2.8%-5.2% and Prime - 0.25% to 0.35% rates maturing to 2032.", "priority": "low", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003", "evidence_required": "Interest-rate risk note: fixed/floating split, hedge accounting, sensitivity to JIBAR/Prime.", "closure_condition": "Rate sensitivity captured; interest expense forecast sensitivity stated."}]}
```

### 5. Baseline Forecast Inputs Captured Here

| Metric (Rm unless stated) | 31 Mar 2026 (Unaudited) | 31 Mar 2025 (Unaudited) | 30 Sep 2025 (Audited) |
| --- | --- | --- | --- |
| Cash and cash equivalents | 112 | 118 | 106 |
| Other investments | 81 | 237 | 41 |
| Trade and other receivables | 497 | 556 | 471 |
| Purchased book debts (total) | 4,489 | 4,353 | 4,677 |
| — Principal book portfolio | 3,845 | 3,690 | 3,975 |
| — Other financial assets (FV) | 644 | 663 | 702 |
| Equity accounted investments | 87 | 109 | 98 |
| Intangible assets | 67 | 82 | 63 |
| Property and equipment | 418 | 495 | 450 |
| Goodwill | 511 | 511 | 511 |
| Deferred tax assets | 173 | 193 | 174 |
| **Total assets** | **6,444** | **6,661** | **6,604** |
| Bank overdrafts | 273 | 457 | 364 |
| Trade and other payables | 221 | 266 | 482 |
| Interest-bearing debt (total) | 3,743 | 3,407 | 3,443 |
| — Senior debt | 3,547 | 3,182 | 3,293 |
| — Subordinated debt | 196 | 225 | 150 |
| Lease liabilities | 345 | 395 | 364 |
| Deferred tax liabilities | 513 | 577 | 551 |
| **Total liabilities** | **5,115** | **5,110** | **5,208** |
| **Total equity** | **1,329** | **1,551** | **1,396** |
| Shares in issue (m) | 780 | 784 | 784 |
| Revenue | 711 | 745 | 1,435 |
| Cost of revenue | (385) | (352) | (732) |
| Gross profit from services | 326 | 393 | 703 |
| Net income from purchased book debts | 69 | 53 | 244 |
| Imputed interest revenue (CAEIR) | 383 | 333 | 683 |
| Interest expense | (177) | (181) | (354) |
| Impairment loss on principal book portfolios | (167) | (173) | (199) |
| Fair value movements on other financial assets | 30 | 74 | 114 |
| Operating costs | (445) | (560) | (1,063) |
| Net finance charge | (39) | (52) | (91) |
| Equity accounted loss | (1) | (43) | (48) |
| Operating loss | (79) | (168) | (186) |
| Non-operating (loss)/profit | (13) | 7 | 38 |
| Loss before tax | (92) | (161) | (148) |
| Income tax | 29 | 39 | 35 |
| Loss from continuing operations | (63) | (122) | (113) |
| Profit/(loss) from discontinued operations | – | 58 | (125) |
| **Loss for the period** | **(63)** | **(64)** | **(238)** |
| Basic LPS continuing (cents) | (8.1) | (15.6) | (14.4) |
| Basic LPS total (cents) | (8.1) | (8.2) | (30.3) |
| Gross collections (principal book) | 773 | 604 | 1,280 |
| Collection costs | 45 | 38 | 83 |
| Net cash collections (principal book) | 728 | 566 | 1,197 |
| Portfolio additions (principal book) | 382 | 265 | 857 |
| Other financial assets additions | 28 | 7 | 84 |
| Other financial assets collections | 116 | 90 | 168 |
| Interest-bearing liabilities total | 4,016 | 3,864 | 3,807 |
| — Payable within 12 months | 1,396 | 1,039 | 1,237 |
| — Payable thereafter | 2,620 | 2,825 | 2,570 |
| Undrawn overdraft facilities | 475 | 43 | 136 |
| Debt raised | 1,145 | 976 | 1,590 |
| Debt settled | (842) | (1,812) | (2,396) |
| Dividends paid | – | – | – |
| Pledged purchased book debts | 3,845 | 3,690 | 3,975 |

**Derived ratios (computed):**
- Collection cost ratio = 45/773 = **5.8%** (H1 2025: 6.3%; FY2025: 6.5%)
- Effective tax rate on loss before tax = 29/(92) = **−31.5%**
- Operating cost change YoY = **−20.5%**
- Revenue change YoY = **−4.6%**
- Gross profit from services change YoY = **−17.0%**
- Equity/total assets = 1,329/6,444 = **20.6%** (31 Mar 2025: 23.3%; 30 Sep 2025: 21.1%)
- Encumbered book debt ratio = 3,845/4,489 = **85.7%** of total purchased book debts pledged

---

### 6. Next Section to Capture

**`D003` (continued) — physical PDF pp. 16–21** (chunk 2 of 5). This will resolve the highest-priority open items: **N1** (ECL allowance and Stage 1/2/3 split), **N2** (impairment decomposition), **N3/N4** (funding covenants, maturity wall, going concern), **N5** (note 6.3 fair value), and the carried-forward D002 questions on ERC methodology, PBD/RTC amortisation, and funding restructuring.