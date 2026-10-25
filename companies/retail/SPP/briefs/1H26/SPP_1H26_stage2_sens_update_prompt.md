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
  "recommendation": "HOLD",
  "reference_price_zar": 92.50,
  "target_price_zar": 104.00,
  "implied_upside_pct": 12.4,
  "forward_dividend_yield_pct": 0.0,
  "projected_12m_tsr_pct": 12.4
}
```

| Metric | Determination | Basis & Key Commentary |
| :--- | :---: | :--- |
| **Sector** | Retail (Retailers — JS4041 / ICB 404010) | Food & staples retailing / consumer staples distribution; voluntary trade wholesale model with integrated retail credit. |
| **Current Reference Share Price** | R92.50 | Reference baseline as at 27 March 2026 reporting date; JSE-listed (SPP / ISIN ZAE000058517). |
| **12-Month JSE Target Price** | R104.00 | Blended valuation: 11.0x FY27E HEPS of 945c (R103.95) cross-checked against DCF (WACC 13.8%, g 3.0%) and 6.5x FY27E EV/EBITDA. |
| **Implied Capital Upside / (Downside)** | +12.4% | Relative to R92.50 reference; reflects recovery from trough earnings, not a re-rating to historical multiples. |
| **Forward Dividend Yield (FY27E)** | 0.0% | Dividend remains suspended per capital hierarchy (Slide 34); resumption only upon positive FCF and gearing <2.0x. |
| **Projected 12-Month TSR** | +12.4% | Capital return only; no distribution assumed in the 12-month window. |
| **Institutional Recommendation** | HOLD | "Show-me" stance: identifiable non-recurring drags and Ireland resilience support trough valuation, but negative FCF, deteriorating debtors' book and unproven KZN recovery cap upside until H2 cash conversion is evidenced. |

---

## 1. EXECUTIVE INVESTMENT THESIS & 12-MONTH JSE PRICE TARGET

**Thesis: A trough-earnings recovery story with a cash-flow asterisk.** SPP's H1 FY2026 operating profit collapse of 47.8% to R730.7m is, on forensic decomposition, ~R216m legacy credit catch-up + ~R212m Black Friday one-off + ~R123m KZN + ~R66m impairments — i.e., largely identifiable and mostly non-recurring. Underlying trading profit of ~R1.0bn (vs R1.40bn) implies a genuine but contained ~29% underlying decline. Ireland (ROCE 17.4%, GP margin +20bps to 13.7%, net debt €44m below 2022 peak) is the stabiliser carrying group returns; SA (ROIC −6.8% pre-IFRS 16) is the value destroyer in need of the turnaround now underway.

**Why HOLD, not BUY:** The two critical junctions from the forensic audit — (i) cash conversion (FCF −R2.0bn, payables-timing flattered by ~R1.8bn) and (ii) the debtors' book (overdues 15.9% vs 13.6%, specific impairment +143% to R273.1m) — are forward risks not yet resolved. The dividend suspension is correct. The UK disposal (A.F. Blakemore, ~£13m gross, net breakeven, removes ~£5m H2 losses and a R1.4bn net liability) genuinely de-risks and completes portfolio simplification. But the investment case now rests on two unproven swing factors: KZN recovery (3 months of profit asserted, unverifiable) and H2 FCF reversal.

**Structural headwinds:** SARB +25bps (May 2026) and ECB +50bps expected raise funding costs (SA average 9.70%, Ireland 3.10%); fuel is 15–18% of W&D costs with H2 hikes flagged; SA grocery discount-format competition intensifying; independent retailer margin pressure feeding directly into the debtor book.

**Structural tailwinds:** Ireland's defensive convenience franchise (38% market share, 1,068 stores, 98.5% service level); SPAR Health +26.1% revenue (137 stores, Project 125 doubling pharmacies); Build-it organic retail +6.1%; R5.57bn debt headroom and R6.64bn total available funding; R33.2m annualised VSP savings against R27.3m cost; Feb–Mar GP growth turned positive (+2.3%) — the first genuine margin-recovery evidence, albeit only two months.

**Valuation anchor:** At R92.50 the stock trades on ~9.8x trough FY26E HEPS (~945c annualised from H1's 199.9c plus a seasonally stronger H2) and ~5.9x FY27E EV/EBITDA — a distressed multiple that already discounts much of the bad news. Our R104 target applies 11.0x FY27E HEPS of 945c, a discount to SPP's historical 12–14x to reflect the unresolved cash/debtors risk, cross-checked by DCF.

---

## 2. DETAILED OPERATIONAL FORECAST (FY27E & FY28E)

**Basis:** FY26E is a 52-week year ending September 2026; H1 actuals (26 weeks to 27 March 2026) are annualised with a seasonally stronger H2 (festive Q1 + KZN stabilisation + UK losses removed from June–Sept). FY27E/FY28E are full forward years. All figures R'm unless stated; continuing operations only (UK/Switzerland/Poland excluded).

| Driver | H1 FY26A | FY26E | FY27E | FY28E | Commentary |
| :--- | :---: | :---: | :---: | :---: | :--- |
| SA merchandise revenue | 50,783 | 103,500 | 108,200 | 113,600 | +1.7% H1 run-rate; FY27 +4.5% on KZN normalisation and Health/Build-it; FY28 +5.0%. |
| Ireland merchandise revenue (ZAR) | 16,699 | 34,000 | 35,700 | 37,500 | €856m H1 at 19.679; FY27 +5.0% ZAR (2.2% EUR volume + FX). |
| Group merchandise revenue | 67,482 | 137,500 | 143,900 | 151,100 | +4.7% FY27, +5.0% FY28. |
| Other revenue (supplier income, fees) | 1,110 | 2,150 | 2,050 | 2,100 | Deliberately normalised down in FY27 as Black Friday supplier-income optimisation is unwound (low-quality stream). |
| **Total revenue** | **68,592** | **139,650** | **145,950** | **153,200** | |
| SA gross margin % | 9.5% | 9.6% | 9.9% | 10.0% | Feb–Mar +2.3% GP growth supports 30–40bps recovery; still below 9.8% H1 FY25. |
| Ireland gross margin % | 13.7% | 13.7% | 13.8% | 13.8% | Vaping/alcohol mix and supplier terms sustain +20bps. |
| **Group gross margin %** | **10.4%** | **10.5%** | **10.7%** | **10.8%** | Blended; SA recovery is the swing. |
| Credit participation (G&L debtor book / SA G&L sales) | ~17% | ~17% | ~16.5% | ~16% | Deliberate de-risking as overdues normalise. |
| Debtor cost % of SA revenue (ECL + write-offs) | 1.1% | 1.0% | 0.8% | 0.7% | H1 R273m specific + R58m write-offs; FY27 assumes no repeat catch-up but elevated baseline. |
| Store count — SA G&L (approx.) | ~1,950 | ~1,960 | ~1,985 | ~2,010 | Net +25/yr; Health +19 stores/yr toward Project 125. |
| Store count — Ireland | 1,068 | 1,070 | 1,075 | 1,080 | Stable; Perrys/Dublin Food Sales bolt-ons. |
| Trading space (m², SA G&L, approx.) | ~2.05m | ~2.06m | ~2.09m | ~2.12m | Modest net adds; refurbishment-weighted. |
| Trading density (R/m², SA G&L wholesale) | ~24,800 | ~50,200 (FY) | ~51,800 | ~53,600 | FY figures annualised; density recovery hinges on KZN service levels. |

**Key operational assumptions:** (1) KZN delivers sustained positive operating profit from month 4 onward, contributing ~R120m FY27 swing vs H1 drag; (2) Black Friday FY27 runs on the new ROI framework with no repeat of the R212m overspend; (3) no further retrospective ECL catch-up — but baseline provisioning stays elevated at ~0.8% of SA revenue; (4) UK losses (~£5m H2 FY26) cease from June–Sept 2026 completion; (5) VSP saves R33.2m annualised from FY27.

---

## 3. CONSOLIDATED FINANCIAL STATEMENTS & CASH FLOW BRIDGE

| R'm (continuing ops) | H1 FY26A | FY26E | FY27E | FY28E |
| :--- | :---: | :---: | :---: | :---: |
| Total revenue | 68,592 | 139,650 | 145,950 | 153,200 |
| Gross profit | 7,112 | 14,660 | 15,620 | 16,550 |
| Gross margin % | 10.4% | 10.5% | 10.7% | 10.8% |
| Operating expenses (net) | (7,542) | (14,050) | (14,300) | (14,850) |
| Operating profit (pre extraordinary) | 882 | 1,850 | 2,320 | 2,650 |
| Extraordinary items | (141) | (250) | (100) | (80) |
| **Operating profit (statutory)** | **741** | **1,600** | **2,220** | **2,570** |
| Net finance costs | (363) | (720) | (680) | (640) |
| Profit before tax | 363 | 880 | 1,540 | 1,930 |
| Taxation (27%) | (71) | (238) | (416) | (521) |
| **PAT (continuing)** | **292** | **642** | **1,124** | **1,409** |
| Shares in issue (m) | 192.5 | 192.5 | 192.5 | 192.5 |
| **HEPS (cents, continuing)** | **199.9** | **~470** | **~945** | **~1,180** |
| DPS (cents) | 0 | 0 | 0 | 250 |
| **Free cash flow to equity (FCFE)** | **(2,012)** | **(600)** | **+850** | **+1,350** |

**Cash flow bridge (FY26E → FY27E):** FY26E FCFE of −R600m reflects H1's −R2,012m partly reversed by H2 payables normalisation (+~R1.4bn), UK loss removal (+~R100m), and capex discipline (~1% of revenue, ~R1.4bn). FY27E FCFE of +R850m assumes: EBITDA ~R3.4bn, working capital neutral (payables timing normalised), capex R1.46bn (1.0% of revenue), net interest R680m, tax R416m. **This is the single most important forecast line** — if FY27E FCFE does not turn positive, the dividend stays suspended and leverage (2.73x reported, likely ~3.0x normalised) approaches the 3.5x covenant.

**Balance sheet trajectory:** Net debt R7.34bn (H1 FY26) → ~R7.0bn (FY26E, UK disposal + H2 FCF) → ~R6.2bn (FY27E) → ~R4.9bn (FY28E). Gearing 2.73x → ~2.6x → ~2.1x → ~1.6x, reaching the 1.5–2.0x medium-term target range by FY28E.

---

## 4. VALUATION MULTIPLES & DCF TABLE

| Valuation Metric | FY26E | FY27E | FY28E | Basis |
| :--- | :---: | :---: | :---: | :--- |
| HEPS (cents, continuing) | 470 | 945 | 1,180 | Recovery from trough; FY27 is the normalised year. |
| P/E at R92.50 | 19.7x | 9.8x | 7.8x | FY26E distorted by trough; FY27E is the anchor multiple. |
| EV/EBITDA | 7.4x | 5.9x | 5.0x | EV = market cap R17.8bn + net debt R7.0bn. |
| Dividend yield | 0.0% | 0.0% | 2.7% | Resumption assumed FY28 at 250c. |
| **DCF per-share value (ZAR)** | — | **R106** | — | WACC 13.8% (RFR 10.5%, ERP 6.0%, beta 1.1, SA risk premium), terminal g 3.0%. |
| **Blended target (ZAR)** | — | **R104** | — | 60% P/E (11.0x × 945c = R103.95) + 40% DCF (R106). |

**DCF assumptions:** FCFF FY27E ~R2.4bn growing to ~R3.0bn by FY31E; WACC 13.8% reflects SA funding cost (9.70% average, 3mJ+1.4–1.7% term margins) and equity risk; terminal growth 3.0% (SA food inflation proxy). The DCF is sensitive to the FY27E FCFE inflection — a one-year delay in cash recovery cuts DCF value by ~R12/share.

**Cross-check:** At R104, the stock trades 11.0x FY27E HEPS — a ~20% discount to SPP's 5-year average forward P/E of ~13.5x, appropriate given unresolved cash/debtors risk but unjustified if H2 FCF reverses as forecast.

---

## 5. SENSITIVITY MATRIX

**Table A: FY27E HEPS (cents) — Sales Growth vs Debtor Cost % of SA Revenue**

| Sales growth \ Debtor cost % | 0.6% | 0.7% | 0.8% (base) | 0.9% | 1.0% |
| :--- | :---: | :---: | :---: | :---: | :---: |
| +3.0% | 1,010 | 985 | 960 | 935 | 910 |
| +4.0% | 1,035 | 1,010 | 985 | 960 | 935 |
| +4.7% (base) | 995 | 970 | **945** | 920 | 895 |
| +5.5% | 1,020 | 995 | 970 | 945 | 920 |
| +6.5% | 1,050 | 1,025 | 1,000 | 975 | 950 |

**Table B: Fair Value (ZAR/share) — FY27E HEPS vs Target P/E Multiple**

| HEPS (c) \ P/E | 9.0x | 10.0x | 11.0x (base) | 12.0x | 13.0x |
| :--- | :---: | :---: | :---: | :---: | :---: |
| 895 | 80.55 | 89.50 | 98.45 | 107.40 | 116.35 |
| 920 | 82.80 | 92.00 | 101.20 | 110.40 | 119.60 |
| **945 (base)** | **85.05** | **94.50** | **103.95** | **113.40** | **122.85** |
| 970 | 87.30 | 97.00 | 106.70 | 116.40 | 126.10 |
| 1,000 | 90.00 | 100.00 | 110.00 | 120.00 | 130.00 |

**Rule of thumb:** Every 75bps swing in group gross margin alters FY27E HEPS by ~95c and fair value by ~R10.50/share. Every 10bps swing in debtor cost % of SA revenue alters HEPS by ~25c and fair value by ~R2.75/share.

---

## 6. ACTIONABLE PORTFOLIO MONITORING TRIGGERS & CATALYSTS

**Operational & Financial Red Lines (thesis-breaking — would trigger de-rating to SELL):**
1. **Debtor overdues breach 18.0%** (from 15.9%) or specific impairment charge exceeds R350m annualised — signals accelerating retailer distress beyond current provisioning; fair value cut to ~R80.
2. **FY26 H2 FCFE fails to reverse to positive** (i.e., full-year FCFE worse than −R1.0bn) — confirms payables timing was structural, not timing; liquidity tightens; fair value cut to ~R75.
3. **Gearing (normalised for payables timing) exceeds 3.2x** or covenant headroom (3.5x) narrows below 0.3x — triggers refinancing risk and likely equity raise; fair value cut to ~R70.
4. **KZN returns to operating loss** for two consecutive months — invalidates the central recovery claim; fair value cut to ~R85.
5. **Group gross margin falls below 10.2%** in FY26 H2 — signals Feb–Mar recovery was not sustained; fair value cut to ~R88.

**Quantified Sensitivity Impacts (rule of thumb):**
- 75bps group gross margin swing = ~95c HEPS = ~R10.50/share fair value.
- 10bps debtor cost % swing = ~25c HEPS = ~R2.75/share fair value.
- 50bps SA sales growth swing = ~40c HEPS = ~R4.40/share fair value.
- 25bps SARB rate move = ~R18m net finance cost = ~9c HEPS = ~R1.00/share.
- R100m working capital outflow = ~52c HEPS-equivalent cash drag = ~R5.70/share FCFE impact.

**Re-Rating Catalysts (upgrade to BUY on evidence):**
1. **H2 FY26 results (Sept 2026):** Positive FCFE, payables normalised, debtors' overdues stabilised below 16%, KZN confirmed profitable for 6+ months — would justify upgrade to BUY with target R120+.
2. **Dividend resumption announcement** — signals board confidence in FCF durability; typically a 5–8% re-rating event.
3. **Gearing below 2.0x** — reaches medium-term target range; removes covenant overhang.
4. **SA gross margin recovery above 10.0%** sustained for two quarters — validates turnaround.
5. **UK disposal completion** (June–Sept 2026) — removes last discontinued-operations drag and ~£5m H2 losses; modest positive.

**Upcoming Milestones & Reporting Dates:**
- **June–Sept 2026:** UK disposal completion (A.F. Blakemore, phased store transfers).
- **September 2026:** FY26 full-year results — the critical H2 FCF and debtors' book verification point.
- **~November 2026:** FY26 AGM.
- **March 2027:** H1 FY27 interim results — first full half under new trade plan and ROI framework.
- **February 2027:** Perrys contingent consideration (R79.5m) payable — cash outflow to monitor.
- **Ongoing:** Monthly SARB/ECB rate decisions; SA food inflation prints (3.4% Mar 2026, accelerating); fuel price adjustments (H2 headwind flagged).

---

## CRITICAL OUTPUT FORMATTING CONSTRAINTS (STRICTLY ENFORCED)

To ensure institutional publication quality and 100% deterministic parsing, you MUST follow these formatting rules:
1. **Mandatory JSON Block First:** Section 1 MUST open with the exact ```json ... ``` summary block containing native float numbers (e.g. `0.42`, `-30.0`), not text descriptions.
2. **Zero HTML Tags:** DO NOT use any HTML tags (`<br>`, `<br/>`, `<span>`, `<div>`, etc.). Use standard Markdown newlines.
3. **Single-Line Table Rows:** Every Markdown table row MUST be on a single continuous line starting and ending with `|`. DO NOT insert blank lines (`\n\n`) within table rows or split cells across multiple lines.
4. **Isolated Determination Cells:** In the Valuation Summary Card, keep determination columns strictly limited to the metric value (e.g. `R0.42` or `-30.0%`). Reserve all commentary and secondary notes strictly for the Commentary column.
5. **No Special Symbols or Arbitrary Code Blocks:** DO NOT wrap ordinary numbers or percentages in backticks (`). Reserve backticks solely for the initial JSON block and formal code/file identifiers.
