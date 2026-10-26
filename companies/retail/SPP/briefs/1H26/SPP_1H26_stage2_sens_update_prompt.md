# STAGE 2-U: INSTITUTIONAL VALUATION SENS UPDATE & RE-RATING
**Target Asset:** SPP Group (SPP)  
**Sector:** Retail  
**Attached Document(s):** `SENS_20260928_S603859.pdf` (SENS / ASX Announcement PDF attached in chat)  
**Base Document:** Established Final Institutional Valuation Report (Provided Below)  
**Task Directive:** SENS Evidence Integration & Generation of New Updated Institutional Valuation Report  

---

### INSTRUCTIONS FOR INSTITUTIONAL RESEARCH ANALYST (LLM):
You are acting as an elite **Managing Director & Head of Retail & Consumer Equity Research** at a premier institutional investment bank.

We are adding a subsequent **SENS / continuous disclosure announcement (PDF attached in chat)** together with our established **Final Institutional Valuation Report** (provided in full below).

A **new updated valuation report** needs to be generated reflecting this new disclosure.

### CORE OPERATING DIRECTIVES:
1. **Analyze the Attached SENS PDF(s):**
   - Read the attached SENS / ASX PDF and extract the key terms, funding milestones, condition precedents (CPs) satisfied, offtake agreements, cash movements, and revised commissioning/production dates.

2. **Evaluate the Valuation & Balance Sheet Impact:**
   - Cross-examine the new evidence against the established Final Valuation Report below.
   - Determine whether the **12-Month Target Price (ZAR)**, **Current Reference Price**, or **Recommendation (BUY / HOLD / SELL)** should be revised or reaffirmed. Quantify the exact financial impact.

3. **Re-Rate Actionable Portfolio Monitoring Triggers:**
   - Review Section 6 ('Actionable Portfolio Monitoring Triggers & Catalysts') of the established report.
   - Mark which triggers have **[FIRED / RESOLVED]** citing the SENS release.
   - Update remaining active triggers and add any new catalysts or operational red lines established by this notice.

4. **Generate the New Updated Valuation Report:**
   - Produce the complete, publication-grade new report incorporating this post-SENS reality.
   - **MANDATORY JSON SUMMARY BLOCK:** You MUST open Section 1 with the following exact machine-readable JSON block containing your updated metrics:
     ```json
     {
       "ticker": "SPP",
       "company_name": "SPP Group",
       "sector": "retail",
       "recommendation": "BUY | HOLD | SELL",
       "reference_price_zar": 0.00,
       "target_price_zar": 0.00,
       "implied_upside_pct": 0.0,
       "forward_dividend_yield_pct": 0.0,
       "projected_12m_tsr_pct": 0.0
     }
     ```
   - **Executive Valuation Summary Card Table:** Follow the JSON block immediately with your updated 4-column comparison table:
     | Metric | Prior (Stage 2) | Updated (Stage 2-U) | Basis & Post-SENS Commentary |
     | :--- | :---: | :---: | :--- |
     | **Sector** | Retail | Retail | [Classification] |
     | **Current Reference Share Price** | R[0.00] | R[0.00] | [Closing date & price] |
     | **12-Month JSE Target Price** | R[0.00] | R[0.00] | [Target price & revision basis] |
     | **Implied Capital Upside / (Downside)** | [+/-0.0]% | [+/-0.0]% | [Relative to reference price] |
     | **Forward Dividend Yield (FY27E)** | [0.0]% | [0.0]% | [Distribution policy & payout] |
     | **Projected 12-Month TSR** | [+/-0.0]% | [+/-0.0]% | [Capital return + dividend yield] |
     | **Institutional Recommendation** | [BUY | HOLD | SELL] | [BUY | HOLD | SELL] | [Primary rating thesis] |

---

## ESTABLISHED FINAL INSTITUTIONAL VALUATION REPORT (GROUND TRUTH)

```json
{
  "ticker": "SPP",
  "company_name": "SPP Group",
  "sector": "retail",
  "jse_sector_code": "JS4041",
  "jse_sector_name": "Retailers",
  "recommendation": "SELL",
  "reference_price_zar": 92.50,
  "target_price_zar": 71.00,
  "implied_upside_pct": -23.2,
  "forward_dividend_yield_pct": 0.0,
  "projected_12m_tsr_pct": -23.2,
  "rating_bands": {
    "strong_buy_max_zar": 54.62,
    "buy_max_zar": 61.74,
    "hold_max_zar": 81.65,
    "sell_max_zar": 74.55,
    "strong_sell_above_zar": 81.65
  }
}
```

| Metric | Determination | Basis & Key Commentary |
| :--- | :---: | :--- |
| **Sector** | Retail (Retailers — JS4041 / ICB 404010) | Food & Drug Retailing — voluntary wholesale & independent retail model (SA G&L, Build it, SPAR Health, Ireland BWG) |
| **Current Reference Share Price** | R92.50 | Indicative JSE close post-H1 FY26 SENS (27 Mar 2026 balance sheet date); reference baseline for rating bands |
| **12-Month JSE Target Price** | R71.00 | Blended: 11.0x FY27E HEPS (R6.45) = R71.00; cross-checked vs DCF (WACC 14.5%, g 3.0%) and 6.5x FY27E EV/EBITDA |
| **Implied Capital Upside / (Downside)** | -23.2% | Target R71.00 vs reference R92.50 |
| **Forward Dividend Yield (FY27E)** | 0.0% | Dividend remains suspended per p.34 capital hierarchy; FCF negative, gearing elevated — no reinstatement before FY28E at earliest |
| **Projected 12-Month TSR** | -23.2% | Capital return only; zero distribution |
| **Institutional Recommendation** | SELL | Contaminated "underlying" earnings, structural cash burn, debtor book distress, pre-IFRS 16 covenant dependency; recovery is price-led and fragile |
| **Dynamic Rating Bands** | Strong Buy: ≤R54.62, Buy: ≤R61.74, Hold: ≤R81.65, Sell: ≤R74.55, Strong Sell: >R81.65 | Anchored to R71.00 target: Strong Buy >30% upside, Buy 15–30%, Hold -5% to +15%, Sell -5% to -15%, Strong Sell >15% downside |

---

### 1. Executive Investment Thesis & 12-Month JSE Price Target

**Thesis: A "Kitchen-Sinked" Balance Sheet Masking a Structural Earnings Reset — SELL.**

The H1 FY2026 result is not a cyclical trough; it is a structural de-rating event. Our forensic read of the primary SENS (p.19, p.25, p.48) confirms that the headline R730.7m operating profit (margin 1.1%) is *flattered* by the classification of ~R331m of credit impairments (R273.1m specific + R58m write-offs) *within* "net operating expenses." The "Operating profit before extraordinary items" of R882.0m is therefore contaminated — the true clean operating profit is closer to **R550m**, implying a clean SA operating margin of ~0.4%, not the 1.3% presented.

Three structural headwinds dominate the 2-year forecast:

1. **The Debtor Book is the Binding Constraint.** G&L overdues surged from 13.6% to 15.9% (p.30) while the specific impairment charge more than doubled to R273.1m. Critically, management confirms credit management enhancements only follow the SAP finance go-live (p.57) — meaning **no near-term ECL relief**. We model debtor costs at 1.35% of SA merchandise revenue in FY27E (vs ~0.9% normalised), a permanent step-up.

2. **The "Genuine Margin Recovery" is Price-Led, Not Volume-Led.** Feb–Mar revenue growth of +2.1% was *below* internal inflation of +2.6% (p.20), confirming real volume contraction at the exit rate. Transactions fell -2.3% (p.56). The recovery is fragile and dependent on promotional discipline that historically has not held.

3. **Cash Burn is Structural, Not Timing.** The R2.0bn FCF outflow was driven by a R1.66bn payables reduction (p.31), artificially inflated by a creditor payment run on 30/31 March (p.28 footnote). This is a genuine cash burn, not a reversal candidate. Net debt at R7.3bn and 2.73x leverage is only "safe" because the covenant is **pre-IFRS 16** (p.55) — excluding R8.4bn of lease liabilities. On a post-IFRS 16 basis, the group would breach.

**Tailwinds (insufficient to offset):** Ireland BWG is a resilient cash generator (€25.3m OP, 3.0% margin, 2.12x gearing, €96.7m headroom); SPAR Health +26.1% revenue; Build it organic +6.1%; UK disposal completes portfolio simplification (broadly breakeven, p.35).

**Verdict:** The market is pricing a recovery that the hard numbers do not support. We initiate at **SELL** with a R71.00 target (-23.2%), implying 11.0x FY27E HEPS of R6.45.

---

### 2. Detailed Operational Forecast (FY27E & FY28E)

**Key modelling assumptions (all ZAR, continuing operations, 52-week basis):**

| Driver | FY26E (H1A + H2E) | FY27E | FY28E | Rationale |
| :--- | :---: | :---: | :---: | :--- |
| SA G&L merchandise revenue growth | +1.5% | +2.8% | +3.5% | Below internal inflation; volume recovery only from H2 FY27 |
| SA Build it revenue growth | +1.5% | +3.0% | +4.0% | Construction cycle trough; micro-credit tailwind |
| SA SPAR Health revenue growth | +26.0% | +18.0% | +15.0% | Project 125 pharmacy roll-out; investment cycle drag on profit |
| Ireland revenue growth (EUR) | +2.2% | +2.5% | +3.0% | Foodservice + convenience resilience |
| Group gross margin % | 10.55% | 10.75% | 10.90% | Modest recovery off BF/KZN lows; not to prior 10.7%+ |
| SA debtor cost % of SA merch rev | 1.35% | 1.30% | 1.20% | Permanent ECL step-up; no SAP relief pre-FY27 |
| SA operating margin % | 0.5% | 1.1% | 1.6% | KZN stabilisation; cost realignment R33.2m annualised saving |
| Ireland operating margin % | 3.0% | 3.1% | 3.2% | Stable; modest opex leverage |
| Store count (SA G&L) | ~2,050 | ~2,075 | ~2,100 | Net +25/yr; refurbishment-led |
| Trading space (m², SA G&L) | ~1.95m | ~1.98m | ~2.01m | Modest net additions |
| Trading density (R/m², SA G&L) | ~R26,500 | ~R27,200 | ~R28,100 | Inflation-led; real density flat |

**Segment operating profit build (R'm):**

| Segment | FY26E | FY27E | FY28E |
| :--- | :---: | :---: | :---: |
| SA G&L operating profit | 180 | 340 | 480 |
| SA Build it operating profit | 95 | 110 | 125 |
| SA SPAR Health operating profit | (15) | 5 | 25 |
| SA Corporate/Other | (60) | (40) | (25) |
| **SA total operating profit** | **200** | **415** | **605** |
| Ireland operating profit (ZAR @ 19.68) | 500 | 520 | 545 |
| **Group operating profit (clean)** | **700** | **935** | **1,150** |
| Group operating margin % | 1.0% | 1.3% | 1.5% |

---

### 3. Consolidated Financial Statements & Cash Flow Bridge

**Group income statement (R'm, continuing operations):**

| Line Item | FY26E | FY27E | FY28E |
| :--- | :---: | :---: | :---: |
| Revenue — merchandise | 134,500 | 139,200 | 145,300 |
| Revenue — other | 2,200 | 2,350 | 2,500 |
| **Total revenue** | **136,700** | **141,550** | **147,800** |
| Gross profit | 14,420 | 15,220 | 16,110 |
| Gross margin % | 10.55% | 10.75% | 10.90% |
| Net operating expenses (incl. ECL) | (13,720) | (14,285) | (14,960) |
| **Operating profit (clean)** | **700** | **935** | **1,150** |
| Extraordinary items (impairments) | (250) | (80) | (40) |
| **Reported operating profit** | **450** | **855** | **1,110** |
| Net finance costs | (720) | (700) | (670) |
| Share of associates | (5) | (3) | 0 |
| **Profit before tax** | **(275)** | **152** | **440** |
| Taxation (27%) | 74 | (41) | (119) |
| **PAT (continuing)** | **(201)** | **111** | **321** |
| Discontinued ops (UK) | (200) | (50) | 0 |
| **Total PAT** | **(401)** | **61** | **321** |
| Shares in issue (m) | 192.5 | 192.5 | 192.5 |
| **HEPS (cents, continuing)** | **~180** | **645** | **1,010** |
| **DPS (cents)** | **0** | **0** | **150** |

**Free Cash Flow to Equity bridge (R'm):**

| Component | FY26E | FY27E | FY28E |
| :--- | :---: | :---: | :---: |
| EBITDA (pre-IFRS 16) | 1,950 | 2,180 | 2,420 |
| Working capital movement | (400) | 150 | 200 |
| Taxation paid | (350) | (280) | (320) |
| Net interest paid | (700) | (680) | (650) |
| Capex (net) | (700) | (720) | (750) |
| Lease payments (principal) | (1,550) | (1,580) | (1,610) |
| **FCFE** | **(1,750)** | **(930)** | **(710)** |
| Disposals (UK) | 250 | 0 | 0 |
| **Net FCFE** | **(1,500)** | **(930)** | **(710)** |

**Key insight:** FCFE remains negative through FY28E. The group cannot reinstate the dividend, cannot buy back shares, and must rely on debt facilities (R5.6bn headroom, p.28) to fund the gap. This is the core of the SELL thesis.

---

### 4. Valuation Multiples & DCF Table

**Blended valuation (ZAR per share):**

| Methodology | Metric | Multiple/Rate | Value (R/share) | Weight |
| :--- | :---: | :---: | :---: | :---: |
| P/E (FY27E HEPS R6.45) | 11.0x | — | 71.00 | 40% |
| EV/EBITDA (FY27E R2,180m) | 6.5x | — | 68.50 | 30% |
| DCF (WACC 14.5%, g 3.0%) | — | — | 74.00 | 30% |
| **Blended target** | | | **71.00** | **100%** |

**DCF assumptions:** WACC 14.5% (RSA risk-free 10.5% + equity risk premium 5.5% × beta 1.1, adjusted for leverage); terminal growth 3.0%; explicit forecast FY27–FY31E; terminal EV/EBITDA 5.5x cross-check.

**Forward multiples at target (R71.00):**

| Metric | FY27E | FY28E |
| :--- | :---: | :---: |
| P/E | 11.0x | 7.0x |
| EV/EBITDA | 6.5x | 5.8x |
| Dividend yield | 0.0% | 2.1% |
| P/B | 2.5x | 2.3x |

**Peer context:** SA food retailers trade 12–15x forward P/E; SPP's discount to target reflects its inferior earnings quality, negative FCF, and covenant dependency. A re-rating to peer multiples is not justified until FCF turns positive.

---

### 5. Sensitivity Matrix

**FY27E HEPS (cents) sensitivity — SA G&L sales growth vs SA debtor cost %:**

| SA G&L Sales Growth ↓ / Debtor Cost % → | 1.10% | 1.20% | 1.30% | 1.40% | 1.50% |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **+1.5%** | 720 | 685 | 650 | 615 | 580 |
| **+2.0%** | 745 | 710 | 675 | 640 | 605 |
| **+2.8% (base)** | 780 | 745 | **645** | 610 | 575 |
| **+3.5%** | 815 | 780 | 745 | 710 | 675 |
| **+4.0%** | 850 | 815 | 780 | 745 | 710 |

**Target price (R/share) sensitivity — FY27E HEPS vs P/E multiple:**

| HEPS (c) ↓ / P/E → | 9.0x | 10.0x | 11.0x | 12.0x | 13.0x |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **580** | 52.20 | 58.00 | 63.80 | 69.60 | 75.40 |
| **645 (base)** | 58.05 | 64.50 | **70.95** | 77.40 | 83.85 |
| **710** | 63.90 | 71.00 | 78.10 | 85.20 | 92.30 |
| **780** | 70.20 | 78.00 | 85.80 | 93.60 | 101.40 |
| **850** | 76.50 | 85.00 | 93.50 | 102.00 | 110.50 |

**Rule of thumb:** Every 75bps swing in SA gross margin alters FY27E HEPS by ~65 cents and fair value by ~R7.15/share (at 11.0x). Every 10bps swing in debtor cost % alters HEPS by ~35 cents and fair value by ~R3.85/share.

---

### 6. Actionable Portfolio Monitoring Triggers & Catalysts

**Operational & Financial Red Lines (thesis-breaking thresholds):**

1. **G&L overdues >17.5%** (currently 15.9%): Would signal accelerating retailer distress and force a further ECL top-up beyond our R273m base case. *Impact: -R8 to -R12/share.*
2. **SA leverage ratio >3.2x** (currently 2.73x, covenant 3.5x): Would compress covenant headroom to <10%, triggering a de-rating and potential facility renegotiation. *Impact: -R10 to -R15/share.*
3. **FCFE outflow >R1.2bn in FY27E** (base case -R930m): Would confirm the cash burn is worsening, not stabilising. *Impact: -R6 to -R9/share.*
4. **SA G&L operating margin <0.8% in H2 FY26** (base case 1.1%): Would invalidate the "genuine recovery" narrative. *Impact: -R5 to -R8/share.*
5. **Dividend reinstatement deferred beyond FY28E**: Confirms capital preservation mandate is structural, not cyclical. *Impact: -R4 to -R6/share.*

**Quantified Sensitivity Impacts (rule of thumb):**

- **Every 75bps swing in SA gross margin** → HEPS ±65c, fair value ±R7.15/share.
- **Every 10bps swing in debtor cost %** → HEPS ±35c, fair value ±R3.85/share.
- **Every 1.0x swing in P/E multiple** → fair value ±R6.45/share.
- **Every R100m swing in SA operating profit** → HEPS ±52c, fair value ±R5.70/share.
- **Every 25bps swing in WACC** → DCF fair value ±R2.80/share.

**Re-Rating Catalysts (upgrade triggers):**

1. **G&L overdues inflect below 14.0%** for two consecutive quarters — signals credit book seasoning.
2. **FCFE turns positive** (requires working capital release + capex discipline) — the single most important catalyst.
3. **SA operating margin sustains >2.0%** for a full half — confirms structural recovery, not price-led bounce.
4. **Dividend reinstatement announced** — signals management confidence in cash generation.
5. **SAP finance go-live completed without disruption** (FY26 H2) — de-risks the FY27 DC integration.

**Upcoming Milestones & Reporting Dates:**

| Date | Event | Significance |
| :--- | :--- | :--- |
| **Sept 2026** | FY26 full-year results (52 weeks to 25 Sept 2026) | First full read on H2 recovery; dividend decision |
| **Nov 2026** | FY26 AGM | Capital allocation vote; board refresh |
| **Dec 2026** | SAP finance go-live (per p.57) | Key operational milestone; credit management enhancement precursor |
| **Mar 2027** | H1 FY27 interim results | First half with SAP finance live; ECL trajectory |
| **May 2027** | Perrys contingent consideration payment (R79.5m) | Cash outflow; Ireland integration check |
| **Sept 2027** | FY27 full-year results | FCFE inflection test; dividend reinstatement window |

---

**Disclaimer:** This note is for institutional informational purposes only and does not constitute investment advice. All forecasts are the analyst's own and subject to material uncertainty given the distressed operational and financial position of SPP Group. The Stage 1 forensic determinations have been treated as the 99% confidence baseline; no material contradictions with the primary SENS were identified that would warrant departure.

---

## CRITICAL OUTPUT FORMATTING CONSTRAINTS (STRICTLY ENFORCED)

To ensure institutional publication quality and 100% deterministic parsing, you MUST follow these formatting rules:
1. **Mandatory JSON Block First:** Section 1 MUST open with the exact ```json ... ``` summary block containing native float numbers (e.g. `0.42`, `-30.0`), not text descriptions.
2. **Zero HTML Tags:** DO NOT use any HTML tags (`<br>`, `<br/>`, `<span>`, `<div>`, etc.). Use standard Markdown newlines.
3. **Single-Line Table Rows:** Every Markdown table row MUST be on a single continuous line starting and ending with `|`. DO NOT insert blank lines (`\n\n`) within table rows or split cells across multiple lines.
4. **Isolated Determination Cells:** In the Valuation Summary Card, keep determination columns strictly limited to the metric value (e.g. `R0.42` or `-30.0%`). Reserve all commentary and secondary notes strictly for the Commentary column.
5. **No Special Symbols or Arbitrary Code Blocks:** DO NOT wrap ordinary numbers or percentages in backticks (`). Reserve backticks solely for the initial JSON block and formal code/file identifiers.
