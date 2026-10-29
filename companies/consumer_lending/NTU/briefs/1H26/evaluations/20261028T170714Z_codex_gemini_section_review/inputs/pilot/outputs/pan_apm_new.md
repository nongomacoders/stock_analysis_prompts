## Section 1 — Key facts and figures

**Scope:** D008.1 (pp. 38–39) is the APM definitions section only — no income statement, cash flow or balance-sheet figures beyond the AISC table. It defines financial APMs, non-financial APMs and ratios, and states APMs are not IFRS measures and may not be comparable across companies.

| Item | Figure | Period / unit | Evidence |
|---|---|---|---|
| Gold share of Group revenue | 99.7% | FY26 | p. 38, "Portfolio complexity" |
| AISC — total lower-cost operations | US$420.686m / 247,219 oz = **US$1,702/oz** | FY26 | p. 39 table |
| AISC — total higher-cost operations | US$87.718m / 25,154 oz = **US$3,487/oz** | FY26 | p. 39 table |
| AISC — Total Group | US$508.405m / 272,373 oz = **US$1,867/oz** | FY26 | p. 39 table |
| AISC — total lower-cost operations | US$241.957m / 168,781 oz = **US$1,434/oz** | FY25 | p. 39 table |
| AISC — total higher-cost operations | US$73.111m / 28,146 oz = **US$2,598/oz** | FY25 | p. 39 table |
| AISC — Total Group | US$315.068m / 196,927 oz = **US$1,600/oz** | FY25 | p. 39 table |

**Arithmetic checks (signed):**
- FY26 Group AISC $m: 420.686 + 87.718 = 508.404 vs stated 508.405 → **+0.001 rounding difference** (immaterial).
- FY26 Group oz: 247,219 + 25,154 = 272,373 ✓.
- FY26 Group $/oz: 508.405 / 272.373 = 1,866.6 ≈ 1,867 ✓.
- FY25 Group $m: 241.957 + 73.111 = 315.068 ✓; oz 168,781 + 28,146 = 196,927 ✓; 315.068/196.927 = 1,599.9 ≈ 1,600 ✓.
- YoY Group AISC/oz: 1,867 − 1,600 = **+US$267/oz (+16.7%)**; Group oz sold +75,446 (+38.3%); Group AISC $m +193.337m (+61.4%). Note the $m growth outpaces oz growth, so unit cost rose despite volume leverage — worth reconciling to cost drivers (not in this capture).

**APM definitions captured (p. 38–39):** AISC, AIC, EBITDA, Adjusted EBITDA, Free cash flow, Levered free cash flow, Headline earnings (SAICA Circular 1/2023), Net (cash)/debt, Net senior debt. AISC is defined per World Gold Council: operating costs plus sustaining capex, less by-product revenue credited against gold cost.

## Section 2 — Footnotes, qualifications and reconciliations

- **AISC is a non-IFRS, WGC-defined measure**; by-product revenue is deducted from operating costs (p. 39). No by-product revenue figure is given here, so the gross operating-cost base behind AISC is not visible in this capture.
- **"Lower-cost" vs "higher-cost" operations split is undefined in this capture** — the grouping basis (asset-level? by mine?) is not stated on pp. 38–39. The higher-cost bucket carries ~9% of oz but ~17% of AISC $m in FY26 (87.718/508.405), and its unit cost is ~2.05× the lower-cost bucket. Scope of the split needs the continuation.
- **Free cash flow definition** includes "less capital expenditure funded through permitted indebtedness" and "less tax paid" (p. 39) — a non-standard deduction; comparability caveat.
- **Net debt** excludes IFRS 9 adjustments, restricted cash and financial liabilities (p. 39) — so reported net debt may differ from a simple borrowings-less-cash calculation.
- **Headline earnings** per SAICA Circular 1/2023 — adjustments listed (disposal P/L, impairments, bargain purchase, tax effect).
- **No reconciliation tables** from APM to IFRS line items appear on pp. 38–39; the AISC table is the only quantified APM here. Reconciliations to "cost of production" are referenced but not shown in this capture.
- **Capture omission vs report omission:** the AISC table is present; the underlying cost-of-production reconciliation and the lower/higher-cost operation definitions are **Pending: D008 continuation (pp. 40–47)**.

## Section 3 — Questions answered and next evidence

No stored questions were supplied. New questions raised (see ledger):

- **Q-AISC-1 (medium):** Basis of "lower-cost" vs "higher-cost" operations split and whether AISC reconciles to IFRS cost of production — target D008 pp. 40–47 and D006.2 segment note.
- **Q-AISC-2 (medium):** Driver of +16.7% YoY Group AISC/oz despite +38% oz sold — need cost-of-production reconciliation and by-product credit — target D008 continuation / D006.2.
- **Q-NETDEBT-1 (low):** Quantified net debt / net senior debt and the IFRS 9 / restricted cash adjustments — target D008 continuation and D005 statement of financial position.

**Next evidence:** Pending: D008 pp. 40–47 (APM reconciliations, non-financial APMs, ratios); D006.2 segment analysis; D005 primary statements.

## Section 4 — Updated Open Questions Ledger

```json
{"ledger_version": 1, "updates": [], "new_questions": [
  {"question": "What is the definition/basis of the 'lower-cost' vs 'higher-cost' operations grouping used in the AISC table, and does Group AISC reconcile to IFRS cost of production (including by-product revenue credit)?", "priority": "medium", "target_document": "Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf", "target_section": "D008 Alternative performance measures (pp. 40-47); D006.2 Note 3 Segment analysis", "evidence_required": "AISC-to-cost-of-production reconciliation table, by-product revenue figure, and definition of lower/higher-cost operation grouping for FY26 and FY25, in US$ and oz.", "closure_condition": "Reconciliation from IFRS cost of production to AISC is shown and the lower/higher-cost grouping basis is stated; or confirmed absent from the report."},
  {"question": "What drove the +16.7% YoY increase in Group AISC per ounce (US$1,600 to US$1,867) despite gold sold rising 38.3% (196,927 to 272,373 oz)?", "priority": "medium", "target_document": "Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf", "target_section": "D008 APM reconciliations (pp. 40-47); D006.2 Segment analysis; D003 CEO statement", "evidence_required": "Breakdown of AISC movement by cost component (operating costs, royalties, sustaining capex, by-product credits) and by operation, FY26 vs FY25, with units and currency.", "closure_condition": "Cost-component or operation-level bridge explains the unit-cost increase, allowing for mix/ramp-up explanations; or confirmed not disclosed."},
  {"question": "What are the quantified net (cash)/debt and net senior debt balances and the IFRS 9, restricted cash and financial liability adjustments excluded from them?", "priority": "low", "target_document": "Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf", "target_section": "D008 APM reconciliations (pp. 40-47); D005 statement of financial position (p. 17)", "evidence_required": "Net debt / net senior debt reconciliation to borrowings and cash, with each adjustment quantified, at 30 June 2026 and 30 June 2025.", "closure_condition": "Reconciliation table with quantified adjustments is provided; or confirmed absent."}
]}
```