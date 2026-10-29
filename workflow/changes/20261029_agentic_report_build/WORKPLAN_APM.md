# WORKPLAN: Alternative Performance Measures (PAN physical pp.38–47) — P0 only

**Status**: P0 blueprint. No extraction of this section is committed. Written after two
failed extraction attempts on p.45, recorded here so the next session starts from the
evidence instead of repeating them.

**Source**: `companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf`
(SHA-256 `62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd`).

---

## 1. What the section contains

| Page | Content | Numeric density |
|---|---|---|
| 38 | Introduction; APM policy and IFRS cross-references | prose only |
| 39 | APM definition matrix (Group APM / IFRS measure / adjustments / rationale) | prose only |
| 40–43 | All-in costs (AIC) by operation, with reconciliation tables | dense |
| 44 | Sustaining capital | dense |
| **45** | **Adjusted EBITDA — definition text plus reconciliation by operation** | **dense, high value** |
| 46 | Net adjusted EBITDA, free cash flow, headline earnings, ratios, NAV per share, levered free cash flow | medium |
| 47 | Return on capital employed | medium |

## 2. Why p.45 is the highest-value page

It repeats the Group production summary operation grid (13 printed value columns:
Barberton, Evander, Total, BTRP, Elikhulu, MTR, Tennant, Total, Barberton total,
Evander total, MTR total, Tennant total, Group total) in US$ million, and reconciles
each column from net income/(cost) before finance to Adjusted EBITDA. It is therefore
the formal definition layer behind both D009 p.50 and Note 3 p.22, and the natural
place to close `Q-c1e6100f7a674873` (APM definitions).

### 2.1 Printed comparison that motivates the extraction

Read directly from the PDF text layer (physical p.45), the FY26 Adjusted EBITDA row prints:

```
142.5  120.9  263.4  29.4  171.4  155.9  43.0  399.7  171.9  292.3  155.9  43.0  663.1
```

D009 physical p.50 prints the same row as:

```
142.4  120.9  263.4  29.4  171.4  155.9  43.0  399.7  171.9  292.3  155.9  43.0  663.1
```

i.e. the **Barberton mining cell differs by 0.1 (142.5 vs 142.4)** while every other
cell and the Group total are identical. Each table is internally consistent on its own
terms: p.45 shows 131.1 net income + 11.4 mining D&A = 142.5, and its leaves sum to
663.1; p.50's leaves sum to 663.0 against its own printed 663.1.

**This is the likely root cause of the 0.1 residual left open since D009 P2** — but it is
NOT yet code-verified, because the p.45 grid is not extracted. It is recorded as an
open `ambiguity` conflict (`APM_EBITDA_BARBERTON|p45|FY26|delta=0.1`) with this page
citation, and must not be stated as proved until an extractor reproduces the row.

## 3. Why the extraction was deferred (failed attempts, recorded)

1. **Fragment rule too narrow.** On p.45 numbers split as `81` + `.5` and `51` + `.8`; a
   regex requiring a leading digit (`^\(?[\d,]*\.?\d+\)?$`) silently dropped the `.5`
   fragment, producing `81` where `81.5` is printed. Fix: accept `.5`-style fragments and
   merge before matching, as the Note 3 extractor does.
2. **Label reconstruction from geometry is wrong on this page.** Wrapped labels print
   *after* the value line (`(Profit)/loss on disposal of plant and` / values /
   `equipment`), so forward-buffering mis-joins them (observed:
   `FY26 equipment Adjusted EBITDA`). The PDF text layer preserves the correct logical
   order; labels should come from the text layer and geometry used only for column
   assignment. A first attempt to zip geometry rows to text-layer rows failed because the
   text-layer regex matched 8 rows against 11 geometry rows — the row-count equality
   assumption is unsafe and needs an explicit row key (e.g. the first numeric value)
   rather than positional zip.
3. **First value column starts left of the value band used elsewhere.** The Barberton
   column ends at x1 ≈ 203.6, so any `x0 >= 250` filter (fine for Note 3) drops it.

Derived geometry for reference (13 edges, tolerance 5.0pt, min count 3):

```
[203.64, 249.13, 294.48, 339.99, 385.19, 487.28, 532.51, 577.88,
 623.27, 668.64, 714.05, 759.28, 804.57]
```

## 4. Planned checks when p.45 is extracted

- **V1 column roll-forward**: net income/(cost) + mining D&A ± disposal loss = Adjusted
  EBITDA, per column, per year.
- **H1 mining subtotal**: Barberton + Evander = Total (cols 0+1 = 2).
- **H2 tailings subtotal**: BTRP + Elikhulu + MTR + Tennant = Total (cols 3..6 = 7).
- **H3 total-operations build**: Barberton total = Mining Barberton + BTRP; Evander total =
  Mining Evander + Elikhulu; MTR total = MTR; Tennant total = Tennant (cols 8..11).
- **H4 group total**: cols 8+9+10+11 = 12.
- **X1 cross-table**: p.45 vs p.50 cell-by-cell, expecting exactly one 0.1 difference
  (Barberton) in FY26 and the FY25 pattern (71.1/16.2/93.9/97.7 vs 71.0/16.3/93.8/97.8).

## 5. P0 acceptance

- [x] Section surveyed (pp.38–47), page roles tabulated.
- [x] Highest-value page identified with justification.
- [x] Printed cross-table discrepancy quoted from the source, explicitly marked unproved.
- [x] Two failed extraction attempts and their causes recorded rather than discarded.
- [x] No partial extraction committed; DB remains at 2,268 cells with the S007 regions only.
