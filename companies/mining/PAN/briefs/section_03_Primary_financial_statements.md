# Section 03: Primary financial statements — SUMMARISED CONSOLIDATED STATEMENT OF FINANCIAL POSITION

> **Package**: `section-d483ba95362948a7bc70a9fa451490e9`  
> **Report**: `Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf` (annual_report)  
> **Model**: `deepseek/deepseek-v4.1-flash-1017`  
> **Execution Time**: 34.42s  
> **Cost**: $0.0023  
> **Tokens**: 12,011 total (7,898 prompt / 4,113 completion)  

### 1. Answers to Stored Questions for This Section

**Q13: Confirm Emmerson acquisition consolidation date (22 June 2026), purchase consideration, goodwill/PPA, FY27 contribution. [D002, p.3]**
- **Status**: `Partially resolved (remainder stays open for D006)`
- **Answer & evidence**: The statement of financial position shows a new **"Shares to be issued"** line of **US$148,218k** in FY26 (nil FY25) `[D005.1, physical PDF p. 17]`, and the statement of changes in equity confirms this was recognised as a non-cash equity-settled addition in FY26 `[D005.1, physical PDF p. 19]`. This is consistent with an acquisition settled in shares (Emmerson) rather than cash — note the cash flow statement shows **no acquisition cash outflow** other than "Cash acquired on acquisitions" of US$12,796k `[D005.1, physical PDF p. 18]`. However, the **consolidation date (22 June 2026), the split of consideration between shares/cash, the goodwill/PPA allocation, and the FY27 contribution are NOT disclosed in this section** — they sit in the business-combinations note (note 18). Goodwill rose only US$1,340k (17,098→18,438) `[D005.1, p. 17]`, which is small relative to a US$148m share consideration, so the PPA/bargain-purchase treatment must be verified in D006. **Remainder stays open for D006.**

*(No other stored questions are answerable from this balance-sheet/P&L/cash-flow/equity capture — all others carried forward to Section 4.)*

### 2. Footnote & Qualification Deep-Dive

- **Cash flow footnote [^1] — dividend re-presentation** `[D005.1, physical PDF p. 18]`: *"The Group changed the presentation of reciprocal dividend cash flows from gross to net during the current reporting period. The comparative figures have been re-presented accordingly."*
  - **What it changes**: The "Dividend paid" line of **(58,540)** FY26 vs (23,675) FY25 is a **net** figure, not gross dividends to all shareholders. It nets off the reciprocal dividend received on treasury shares held by PAR Gold (13.1% holder). This means the cash-flow dividend line **cannot** be reconciled directly to the equity "Dividends paid" of (67,387) `[D005.1, p. 19]` without adding back the reciprocal dividend of 8,847. Check: 67,387 − 8,847 = 58,540 ✓ — arithmetic ties. **Implication for forecast**: model dividend cash outflow on a net basis; do not gross up. Verify in D006 (note 22 related party) that the reciprocal dividend is a genuine cash round-trip and not a permanent exclusion.

- **Equity footnote [^1] — Reciprocal dividend – PAR Gold** `[D005.1, physical PDF p. 19]`: PAR Gold holds **13.1%** of issued share capital; the reciprocal dividend (8,847 FY26; 3,784 FY25) is an intra-group dividend on treasury shares. **Implication**: this is a related-party circular flow that inflates both dividend paid and a retained-earnings credit; it should be eliminated in a clean free-cash-flow-to-equity view. Verify note 22.

- **Equity footnotes [^2]/[^3]/[^4] — numbering mismatch** `[D005.1, physical PDF p. 19]`: The table uses markers [^1], [^2], [^3], [^4] but the printed footnote definitions are labelled [^1], [^3], [^4] with **no [^2] definition visible** and the "Refer to note 15" / "Refer to note 14" mapping is ambiguous (share buy-back and shares-to-be-issued both tagged [^3]). **This is a capture/presentation gap** — the exact note cross-references for capital reduction, buy-back and shares-to-be-issued must be confirmed in D006 (notes 14/15). Do not assume.

- **"Shares to be issued" US$148,218k** `[D005.1, p. 17 & 19]`: A large non-cash equity item with **no cash flow**. It sits in equity but is not yet share capital — dilution/issuance mechanics and whether these are Emmerson consideration shares must be confirmed (note 14/15, D006). This materially affects **share count for FY27 EPS and dividend per share**.

- **Share-based payment obligations jump**: non-current 10,297→20,385 and current 11,190→43,969 (total ~64.4m vs ~21.5m) `[D005.1, p. 17]`. This is a large balance-sheet build; the P&L charge sits in "Other expenses" (85,958 vs 36,484) — quantify in D006 (note 17) for Q12.

- **Deferred tax liabilities** 140,506→250,480 (+~110m) `[D005.1, p. 17]` alongside a deferred tax **asset** of only 1,921 — a large timing difference build (likely PPE/EMA); relevant to FY27 effective tax rate modelling. Verify in note 6.2.

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| Q22 | High | D006 (Financial notes) | "Shares to be issued" US$148,218k, no cash flow; likely Emmerson consideration `[D005.1, p. 17, 19]` | In note 14/15 and note 18, confirm what the shares-to-be-issued relate to, number of shares, issue price, and timing of actual issuance | Determines FY27 diluted share count, EPS and DPS |
| Q23 | High | D006 (Financial notes) | Goodwill only +1,340k despite US$148m share consideration; PPA/bargain purchase `[D005.1, p. 17]` | In note 18 (business combinations), confirm Emmerson consideration split, fair value of net assets acquired, goodwill vs bargain gain, consolidation date (22 Jun 2026) | Sets FY27 consolidation contribution and any PPA amortisation |
| Q24 | High | D006 (Financial notes) | Dividend cash flow net (58,540) vs equity dividends (67,387); reciprocal 8,847 `[D005.1, p. 18–19]` | In note 22, confirm reciprocal dividend is a cash round-trip on 13.1% treasury holding; confirm net vs gross presentation and FY27 dividend policy | Correct FCFE and dividend forecast; avoid double-count |
| Q25 | Medium | D006 (Financial notes) | SBP obligations build to ~64.4m; "Other expenses" 85,958 vs 36,484 `[D005.1, p. 17–18]` | In note 17, extract FY26 SBP P&L charge and FY27 expected charge; confirm what drives "Other expenses" increase | FY27 cost base and AISC (Q12) |
| Q26 | Medium | D006 (Financial notes) | Deferred tax liability +110m to 250,480 `[D005.1, p. 17]` | In note 6.2, confirm drivers (PPE/EMA timing) and FY27 effective tax rate | FY27 tax charge and cash tax |
| Q27 | Medium | D006 (Financial notes) | Footnote numbering gap ([^2] undefined; [^3]/[^4] ambiguous) `[D005.1, p. 19]` | Confirm note 14 (share capital/shares to be issued) and note 15 (reserves/buy-back) cross-references | Resolves equity movement mechanics |
| Q28 | Medium | D006 (Financial notes) | Short-term investments 137,867 and investments 12,791 new in FY26; restricted cash 2,612 `[D005.1, p. 17–18]` | In notes 9/13, confirm nature/liquidity of short-term investments and whether available for capex/dividends | Adjust net debt / available liquidity for forecast |
| Q29 | Low | D006 (Financial notes) | Contract liability 8,030 new; other receivables 15,496→41,654 `[D005.1, p. 17]` | In notes 11/12/4, confirm drivers (prepayments, offtake, Emmerson) | Working-capital forecast |

### 4. Updated Open Questions Ledger (Copy to App)

```markdown
# OPEN QUESTIONS LEDGER — after D005.1 (Primary financial statements)

## Pending: D006 (Financial notes)
- Q3: Reconcile dividend implied share counts: 2,436m (final), 2,333m (interim), 2,420m (total); check issued/weighted count, Emmerson shares, treasury. [D002, p.2]
- Q4: Confirm FX rate/date used for dividend US$ conversion (implied ~16.40–16.46 vs stated avg 16.90). [D002, p.2]
- Q8: Confirm Soweto Cluster DFS gold price assumption; FID timing Dec 2026; financing plan; capex post-FY27. [D002, p.3]
- Q12: Quantify share-based payment expense FY26 vs FY25 and FY27 assumption. [D002, p.3]
- Q16: Locate Tennant FY27 capex $ for fixed crusher, secondary mill, belt filter; confirm capitalised vs expensed. [D003, p.6]
- Q19: Extract total FY27 group capex guidance and Tennant-specific split from capex note. [D003, p.6]
- Q13 (remainder): Confirm Emmerson consolidation date (22 Jun 2026), consideration split (shares vs cash), goodwill/PPA/bargain treatment, FY27 contribution. [D002, p.3; D005.1, p.17,19]
- Q22: Confirm what "Shares to be issued" US$148,218k relates to (Emmerson?), number of shares, issue price, timing of issuance. [D005.1, p.17,19]
- Q23: Confirm Emmerson consideration split, fair value of net assets, goodwill vs bargain gain, consolidation date. [D005.1, p.17]
- Q24: Confirm reciprocal dividend (8,847) is cash round-trip on 13.1% treasury; net vs gross presentation; FY27 dividend policy. [D005.1, p.18–19]
- Q25: Extract FY26 SBP P&L charge and FY27 expected charge; explain "Other expenses" 85,958 vs 36,484. [D005.1, p.17–18]
- Q26: Confirm deferred tax liability +110m drivers and FY27 effective tax rate. [D005.1, p.17]
- Q27: Confirm note 14/15 cross-references (footnote numbering gap [^2] undefined). [D005.1, p.19]
- Q28: Confirm nature/liquidity of short-term investments 137,867 and investments 12,791; restricted cash 2,612. [D005.1, p.17–18]
- Q29: Confirm drivers of contract liability 8,030 and other receivables 41,654. [D005.1, p.17]

## Pending: D008 (Alternative performance measures)
- Q2: Obtain AISC reconciliation (by operation and group); confirm inclusions/exclusions (royalties, SBP, third-party processing) vs guidance US$1,820–1,870/oz. [D002, p.3]
- Q11: Confirm renewable energy US$5.1m is in FY26 base (not additive to FY27); water savings US$1.4m/yr is incremental FY27+. [D002, p.2–3]
- Q20: Reconcile Elikhulu US$1,231/oz, MTR US$1,389/oz, BTRP US$1,564/oz to group AISC; confirm BTRP cost spike drivers. [D003, p.6]

## Pending: D009 (Group production summary)
- Q1: Confirm total group ounces, Sheba+Consort ounces and their AISC; reconcile to implied ~US$3,500/oz tail (90.8% at US$1,702/oz vs group US$1,867/oz). [D002, p.2–3]
- Q6: Confirm Elikhulu 56,475oz @ US$1,231/oz and MTR 51,927oz @ US$1,389/oz are full-year; check MTR expansion (Dec 2025) run-rate into FY27. [D002, p.3]
- Q9: Reconcile White Devil ~3Mt @ 3.8g/t (~350Koz) to 50→100Koz/yr ramp over 5 years; check implied LoM. [D002, p.3]
- Q5 (remainder): Confirm Tennant FY27 capex $ amounts; White Devil first blast date (Aug 2026?) and grade ramp. [D002, p.3; D003, p.6]
- Q7 (remainder): Confirm Evander underground grade >11g/t FY26 sustainability into FY27; repeatable or one-off. [D002, p.3]
- Q10 (remainder): Confirm Royal Sheba first production timing (first blast early 2027) and whether any FY27 ounces; confirm not double-counted with BTRP. [D002, p.3; D003, p.6]
- Q14: Check FY27 MTR production split; confirm H1 FY27 below nameplate, Q2–Q4 step-up to ~60Koz annualised post calcine clearance. [D003, p.6]
- Q15: Check FY27 BTRP guidance; confirm whether flotation (complete end-CY2026) benefit assumed in FY27 or FY28. [D003, p.6]
- Q17: Check Elikhulu FY27 guidance vs FY26 56,475oz; confirm Winkelhaak feed volume contribution. [D003, p.6]
- Q18: Check FY27 Tennant grade assumption and White Devil strip ratio/grade in production summary. [D003, p.6]
- Q21: Confirm Fairview 47,678oz vs table 47,677oz rounding; which figure used in group total. [D003, p.6–7]
```

### 5. Baseline Forecast Inputs Captured Here

| Item | FY26 | FY25 |
| --- | --- | --- |
| Revenue (US$k) | 1,156,451 | 540,033 |
| Cost of production (US$k) | (514,297) | (314,187) |
| Gross profit (US$k) | 642,154 | 225,846 |
| Other expenses (US$k) | (85,958) | (36,484) |
| Royalty costs (US$k) | (14,609) | (5,106) |
| Finance income / costs (US$k) | 5,848 / (17,318) | 1,856 / (21,073) |
| Profit before tax (US$k) | 534,368 | 196,633 |
| Income tax expense (US$k) | (177,457) | (56,028) |
| Profit for period (US$k) | 356,911 | 140,605 |
| Basic & diluted EPS (US cents) | 17.60 | 7.16 |
| Net cash from ops before div/tax/roy/finance (US$k) | 712,119 | 223,184 |
| Net cash from operating activities (US$k) | 556,991 | 154,860 |
| Capex: PPE payments (US$k) | (189,723) | (153,989) |
| Exploration payments (US$k) | (26,030) | (3,921) |
| Net cash used in investing (US$k) | (352,144) | (149,851) |
| Net cash used in financing (US$k) | (155,874) | 17,457 |
| Cash & equivalents at 30 Jun (US$k) | 108,312 | 49,532 |
| Borrowings non-current / current (US$k) | 38,578 / 12,957 | 103,642 / 86,335 |
| Short-term investments (US$k) | 137,867 | – |
| Total equity (US$k) | 1,035,997 | 546,668 |
| Shares to be issued (US$k) | 148,218 | – |
| SBP obligations non-current / current (US$k) | 20,385 / 43,969 | 10,297 / 11,190 |
| Deferred tax liabilities (US$k) | 250,480 | 140,506 |
| Dividends paid (equity, US$k) | (67,387) | (27,459) |
| Reciprocal dividend PAR Gold (US$k) | 8,847 | 3,784 |
| Dividend paid (cash flow, net, US$k) | (58,540) | (23,675) |
| PAR Gold holding | 13.1% | 13.1% |

### 6. Next Section to Capture

**D006 (Financial notes, physical pp. 19–36)** — resolves the highest-priority open items: **Q13 (remainder), Q22, Q23, Q24, Q25, Q26, Q27, Q28, Q29**, plus carried-forward **Q3, Q4, Q12, Q16, Q19**. This is the single most valuable next capture because it contains the business-combination (Emmerson), share capital, SBP, tax and related-party notes needed to lock down FY27 share count, cost base and consolidation contribution.