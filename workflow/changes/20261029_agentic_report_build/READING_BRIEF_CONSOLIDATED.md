# Consolidated Reading Brief — Pan African Resources FY26 (built sections only)

**Source**: `companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf`
(SHA-256 `62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd`).
**Sections covered**: D009 Group production summary (pp.48-50) · S006 primary statements (pp.17-18) ·
S007 Note 3 segment analysis (pp.21-24) · APM (pp.40-47) · Notes 4, 7, 16, 17 (pp.25, 27-28, 32-34).
**Lineage**: every figure below is a printed cell in `build/report.sqlite` (4,800 cells). Every arithmetic
statement is executed by `tests_reconcile/` (109 tests, exit 0). Nothing is quoted from model memory.

> **Reading rule for this brief.** Figures drawn from sections whose identities are executed in the suite are
> stated plainly. Figures drawn from the thirteen *extracted-but-unverified* pages (pp.4, 6, 9, 10, 19, 26, 29,
> 30, 31, 34, 35, 36, 39) are marked **[printed, unverified]**. No unverified figure drives a conclusion here.

---

## 1. What the company reports

**Production and sales (D009)**

| | FY26 | FY25 |
|---|---|---|
| Group gold produced | 272,310 oz | 196,527 oz |
| Group gold sold | 272,373 oz | 196,926 oz |
| Group realised price | US$4,235/oz | US$2,735/oz |
| Cash cost | US$1,600/oz | US$1,426/oz |
| AISC | US$1,867/oz | US$1,600/oz |
| All-in cost | US$2,576/oz | US$2,383/oz |

**Financial statements (S006)**

| | FY26 | FY25 |
|---|---|---|
| Revenue | US$1,156,451k | US$540,033k |
| Cost of production | US$(514,297)k | US$(314,187)k |
| Gross profit | US$642,154k | US$225,846k |
| Operating profit | US$545,838k | US$215,850k |
| Profit before tax | US$534,368k | US$196,633k |
| Profit for the period | US$356,911k | US$140,605k |
| Total comprehensive income | US$400,965k | US$155,554k |
| Basic and diluted EPS | 17.60 US cents | 7.16 US cents |
| Cash generated from operations | US$556,991k | US$154,860k |
| Closing cash | US$108,312k | US$49,532k |
| Total assets = total equity and liabilities | US$1,608,075k | US$1,004,509k |

**Balance sheet structure (S006)** — total equity US$1,035,997k; non-current liabilities US$349,328k;
current liabilities US$222,750k. PPE carrying amount US$1,196,474k (Note 7: cost US$1,536,566k less
accumulated depreciation US$340,092k).

**Returns and per-share (APM)** — ROCE 59.8% (FY25 35.1%); NAV per share 51.10 US cents (FY25 26.94);
levered free cash flow US$201.8m (FY25 US$47.5m); cash flow per share 9.95 US cents; cash flow yield 7.96%.

**Capital (APM p.44)** — total capital US$224.0m (FY25 US$167.9m), of which sustaining US$21.8m and
expansion US$202.2m. Net cash US$(185.7)m at year end (FY25 net debt US$150.5m); net senior cash US$(194.7)m.

**Segment shape (S007)** — mining operations revenue US$1,155,857k plus Agricultural ESG US$594k equals the
group total. Barberton US$352,807k; Evander US$441,978k; MTR US$228,268k; Tennant US$132,804k.
Segment assets US$1,589,637k plus goodwill US$18,438k equals total assets exactly.

---

## 2. What reconciles, and therefore what can be relied on

These were executed as code, not asserted:

1. **Balance sheet identity** holds both years: assets equal equity plus liabilities to the dollar.
2. **Income statement cascade** holds: revenue to gross profit to operating profit to profit before tax to
   net profit, and to total comprehensive income.
3. **Cash flow** rolls: operating US$556,991k, investing US$(352,144)k and financing US$(155,874)k give
   US$48,973k; opening US$49,532k plus that plus FX US$9,807k equals closing US$108,312k — which equals the
   balance-sheet cash line.
4. **Segment analysis** ties horizontally on all 72 rows, and vertically to the primary statements on seven
   independent lines.
5. **All-in cost definition chain** holds: cash cost equals gold cost of production; AISC builds from it;
   AIC adds voluntary severance (FY25) and expansion capital. FY25 ties exactly; FY26 has six printed
   half-cent cells, recorded.
6. **PPE** roll-forwards in both years across all fourteen columns, and cost less accumulated depreciation
   equals the carrying amount that appears on the face.
7. **Note 4 revenue** disaggregates to the group total by commodity and by geography, both years.
8. **Note 16** instrument roll-forwards all balance, and the credit facility listing sums to its printed total.
9. **ROCE** rebuilds from printed inputs, and both denominators trace elsewhere: average equity to the
   balance sheet, average borrowings to the net debt table.

---

## 3. What does not reconcile — 97 recorded conflicts

The build never overwrote a printed figure. Where two printed numbers disagree, both are kept.

**Material (carry into any analysis):**

- **Adjusted EBITDA is published at two scopes.** Note 3 (p.22) prints US$609,431k for the group; the
  production summary (p.50) prints US$663.1m. The gap is US$53.670m and is exactly the five non-operating
  columns — Solar 988, Exploration 222, ESG 345, Corporate 51,884, Funding 231 (US$'000). D009 measures the
  operating segments only; its four segment cells (171.9 + 292.3 + 155.9 + 43.0) reproduce 663.1. **Use 663.1
  for operating performance and 609.4 for group-level earnings quality** — they are not interchangeable.
- **Barberton total operations FY26 prints 94,929 oz against components of 84,929 oz** (underground 71,997 +
  BTRP surface 12,932). The 10,000 oz difference also appears in the operations-sum: the four segment totals
  add to 282,310 against a printed group total of 272,310. Substituting 84,929 makes it tie exactly, which is
  conditional agreement only — the printed figure is not corrected. Open as `Q-1f48aa6d4b884f09`.
- **MTR FY25 prints 25,043 oz of tailings production but 30,806 oz of total operations.** The 5,763 oz gap
  equals FY26's printed MTR buy-in exactly, and balances the surface tailings row (92,873 + 5,763 = 98,636).
  Arithmetic consistency, not causation. `Q-3e8730dbd1994205` stays open.
- **FY25 group gold sold differs between two tables**: 196,926 oz on p.49, 196,927 oz on p.43. One ounce.
- **Note 16.3 DMTN closes US$51,475k (38,579 non-current / 12,896 current)** against face borrowings of
  38,578 and 12,957 (51,535) — three printed differences of −1, +61 and −60. The note covers DMTN only.

**Riverbed detail (does not change any total):** eleven ±0.1 cells across pp.40-44 and p.50, each recorded
with its page and asserted as an exact set, so a new one cannot appear unnoticed. The ADJUSTED EBITDA 142.5
on p.45 versus 142.4 on p.50 is the root cause of a 0.1 leaf-sum residual that sat unexplained for most of
this build; it is now proved.

---

## 4. What an analyst should question

1. **Why does Barberton's total operations column exceed its own components by exactly 10,000 oz in a year
   when the prior year ties?** A round number suggests a systematic treatment, not a typo. The prior year
   ties at 68,549 + 15,224 = 83,773.
2. **Is the FY25 MTR gap a buried buy-in?** The 5,763 oz figure appears as an explicit FY26 buy-in line and
   as nil in FY25. If FY25 genuinely had no buy-in, something else sits inside that 30,806.
3. **Which Adjusted EBITDA is the headline?** The company leads with 663.1; Note 3's own reconciliation shows
   609.4 once corporate and funding costs are included. Levered free cash flow is built on 609.4.
4. **Does the Elikhulu FY25 all-in cost of 68,843 ZAR/kg hold?** At 18.17 US$/ZAR and 1,172 US$/oz it implies
   roughly 684,658 ZAR/kg — an order of magnitude away, consistent with an omitted digit. `Q-f1a4ce3647724ed9`.
5. **The Funding Company's net assets flip from (105,951) to 137,658 US$'000.** Not explained by anything in
   the extracted pages; Note 16 shows the facilities closing at nil, so the swing sits somewhere else.

---

## 5. Ledger status

| ID | Priority | State | Basis |
|---|---|---|---|
| `Q-e8c872e6edc94d18` | medium | **Resolved** | Evander total 27,829 = 26,748 + 1,081; the same 1,081 is inside group underground 93,724 |
| `Q-a0b503d7ac044eee` | high | **Substantially resolved** | Segment-level bridge proved: mining ops 1,155,857 + ESG 594 = 1,156,451; ZAR translation basis still pending |
| `Q-ced8d2566db6459c` | low | **Partial** | FY25 Tennant EBITDA swing decomposed (30,342 → 2,443 via 28,019 bargain purchase + 120 derivative); A$/kg swing separate |
| `Q-c1e6100f7a674873` | high | **Partial** | Scope difference proved arithmetically; formal definition wording still to be quoted |
| `Q-1f48aa6d4b884f09` | medium | **Open** | 10,000 oz Barberton discrepancy; conditional agreement only |
| `Q-3e8730dbd1994205` | medium | **Open** | 5,763 oz MTR gap; arithmetic consistent, cause unproved |
| `Q-f1a4ce3647724ed9` | medium | **Open** | Elikhulu 68,843 ZAR/kg magnitude anomaly |
| `Q-c5e1b41b1cfe4dfb` | medium | **Open** | Tennant consolidation into group ZAR revenue |

**Next evidence**: Note 16 (pp.32-33) for the Funding swing; Note 3 (pp.21-24) for the Barberton column;
APM definitions (p.39) for the wording of 5.

---

## 6. Limits of this brief

- Thirteen pages are extracted with printed values and lineage but **no executed identity**; they are marked
  **[printed, unverified]** and no conclusion here rests on them.
- Pages 37 (contents), 38 and 51 (prose) carry no figures.
- The question ledger's *definitions* remain prose questions; arithmetic cannot close them.
- This is a reconciliation of one section group in one announcement, not a valuation. No forecast, no target,
  no view on the shares.
