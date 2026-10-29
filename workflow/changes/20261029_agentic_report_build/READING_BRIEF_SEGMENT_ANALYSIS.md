# Reading Brief: Pan African Resources — Note 3 Segment Analysis (Section S007)

**Target Section**: Section S007 (Note 3 Segment Analysis, physical pages 21, 22, 23, 24; printed pages 34–41 area).  
**Source Document**: `companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf` (SHA-256 `62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd`).  
**Reporting Unit**: US$ thousand (`US$ '000`).  
**Artifact Lineage**: generated from `build/report.sqlite` (extraction `p1_note3_segments_v2`, reconciliation commit `4b94f70`). Every total below executed by `tests_reconcile/test_note3_segments.py` (52/52 suite green).

---

### 1. Key Facts and Figures

**Segment columns** (identical grid on all four pages): Barberton Mines, Evander Mines, Solar projects, MTR operation, Tennant Mines → *Mining operations subtotal*; then Exploration assets, Agricultural ESG projects, Corporate, Funding Company → *Group total*.

**FY26 profitability (p.21, US$ '000)**

| Line | Barberton | Evander | Solar | MTR | Tennant | Mining ops | ESG | Corporate | Funding | Group |
|---|---|---|---|---|---|---|---|---|---|---|
| Revenue | 352,807 | 441,978 | – | 228,268 | 132,804 | 1,155,857 | 594 | – | – | 1,156,451 |
| Cost of production | (176,537) | (162,691) | (2,373) | (79,899) | (91,610) | (513,110) | (1,187) | – | – | (514,297) |
| Gross profit | 176,270 | 279,287 | (2,373) | 148,369 | 41,194 | 642,747 | (593) | – | – | 642,154 |
| Profit before tax | 158,346 | 275,377 | (2,448) | 139,116 | 23,836 | 594,227 | (1,025) | (52,088) | (6,524) | 534,368 |
| Income tax | (50,997) | (77,439) | (1,996) | (38,605) | (8,512) | (177,549) | – | 809 | (717) | (177,457) |

**FY26 balance sheet, capex and EBITDA (p.22, US$ '000)**

| Line | Barberton | Evander | Solar | MTR | Tennant | Mining ops | Exploration | ESG | Corporate | Funding | Group |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Segment assets | 246,642 | 516,518 | 29 | 192,093 | 345,073 | 1,300,355 | 596 | 2,535 | 96,545 | 189,606 | 1,589,637 |
| Segment liabilities | 110,388 | 189,832 | 6,991 | 84,562 | 75,204 | 466,977 | 14 | 53 | 53,086 | 51,948 | 572,078 |
| Net assets (excl. goodwill) | 136,254 | 326,686 | (6,962) | 107,531 | 269,869 | 833,378 | 582 | 2,482 | 43,459 | 137,658 | 1,017,559 |
| Goodwill | 18,438 | – | – | – | – | 18,438 | – | – | – | – | 18,438 |
| Capital expenditure | 40,081 | 70,941 | 7,159 | 32,599 | 71,304 | 222,084 | – | 78 | 1,833 | – | 223,995 |
| Adjusted EBITDA | 171,874 | 292,316 | (988) | 155,899 | 43,012 | 662,113 | (222) | (345) | (51,884) | (231) | 609,431 |

**FY25 comparatives (pp.23–24)**: revenue 540,033; cost of production (314,187); gross profit 225,846; profit before tax 196,633; segment assets 987,411; segment liabilities 457,841; net assets 529,570; goodwill 17,098; capex 167,909; adjusted EBITDA group 226,584 (operating segments 245,765).

---

### 2. Footnotes, Qualifications and Reconciliations

1. **Every segment row ties horizontally, exactly.** For all 72 extracted segment rows across the four pages, columns 0–4 sum to the Mining operations subtotal and the subtotal plus Exploration, ESG, Corporate and Funding sums to Group total, with zero residual. This is executed as a code check, not asserted.

2. **Note 3 ties to the primary statements (S006).** Group revenue 1,156,451, cost of production (514,297), operating profit 545,838, profit before tax 534,368, tax (177,457) and net profit 356,911 all equal the income statement. Segment assets 1,589,637 + goodwill 18,438 = total assets 1,608,075; segment liabilities 572,078 = non-current 349,328 + current 222,750; net assets 1,017,559 + goodwill 18,438 = total equity 1,035,997.

3. **Adjusted EBITDA is printed at two scopes — and the gap is now fully explained, not merely flagged.** Note 3 Group total is 609,431 (US$609.4m) while the Group production summary (p.50) prints 663.1 US$m. The difference is the five non-operating columns, all printed: Solar (988), Exploration (222), ESG (345), Corporate (51,884) and Funding (231) = 53,670. Note 3 operating segments alone are 171,874 + 292,316 + 155,899 + 43,012 = 663,101 → 663.1, which is exactly the p.50 figure. FY25 reproduces identically (93,798 + 97,761 + 51,763 + 2,443 = 245,765 → 245.8).

4. **This also closes the 0.1 residual carried open from the D009 pass.** The p.50 Group total is the sum of *unrounded* segment figures, while the printed p.50 leaf cells are individually rounded to one decimal, so the printed leaves add to 663.0 rather than 663.1. The earlier "0.1 mismatch" is therefore a rounding artefact of the summary table, demonstrated arithmetically. Both printed values remain untouched.

5. **Tennant's FY25 adjusted EBITDA is nearly eliminated by printed adjustments**: EBITDA 30,342 → adjusted 2,443, a swing of 27,899 made of the 28,019 bargain purchase gain exclusion plus a 120 unrealised fair value derivative loss. Group-level the same reconciliation runs 249,724 + 2,954 impairment − 28,019 bargain purchase + 1,925 derivative = 226,584.

6. **A second, differently-structured block sits below the segment table on pp.21 and 23** ("Revenue … excluding intra-Group transactions", "Cost of production", "Elimination of dividends received from/(paid to) fellow Group companies"). Its columns are not segment columns, so it is extracted to the separate region `note3_intra_group` and excluded from the segment identities rather than silently forced into the grid. Recorded as an ambiguity conflict (`Q-a0b503d7ac044eee`).

7. **Retained losses in the Funding Company are visible**: FY25 Funding net assets are (105,951) versus FY26 137,658, and FY25 Funding profit before tax is (16,352) versus FY26 (6,524). The Funding entity's equity position flips sign year on year on printed figures — worth verifying against Note 16 borrowings (`Pending: S009/p.32–33`).

---

### 3. Questions Answered and Next Evidence

- `Q-a0b503d7ac044eee` [high]: **Substantially resolved.** The IFRS-to-segment bridge is now proved at segment level, not just in aggregate: mining operations revenue 1,155,857 + ESG 594 = Group 1,156,451 vs p.50's 17,249.1 ZARm. The remaining ZAR translation difference is a currency-presentation matter, not a consolidation hole. Residual: confirm the ZAR/US$ translation basis used for the p.50 table (`Pending: S010/p.38–39` APM section).
- `Q-c1e6100f7a674873` [high]: **Partial.** Adjusted EBITDA scope is now demonstrated arithmetically (operating segments only in D009; full segment including Corporate/Funding in Note 3). Formal APM definition wording still to be captured (`Pending: S010/p.45`).
- `Q-1f48aa6d4b884f09` [medium]: **Unchanged / still open.** Note 3 revenue confirms the Barberton segment at 352,807 with no separate line that would account for the 10,000 oz production gap; the gap is a production-column matter, not a revenue one.
- `Q-c5e1b41b1cfe4dfb` [medium]: **Partial.** Tennant is now visibly consolidated as its own revenue column (132,804 FY26 vs 3,873 FY25) and capex column (71,304 vs 35,849). Currency of the Note 3 presentation is USD throughout, so the A$ disclosure on p.50 remains a separate presentation.
- `Q-ced8d2566db6459c` [low]: **Partial.** The FY25 Tennant EBITDA-to-adjusted-EBITDA swing (30,342 → 2,443) is now fully decomposed in printed figures (28,019 bargain purchase exclusion, 120 derivative loss). The A$/kg all-in cost swing remains a separate unit-cost matter, unchanged.

**Next Evidence**: `Pending: S009/p.32–33` (Note 16 borrowings — Funding Company reversal), `Pending: S010/p.38–45` (APM definitions).
