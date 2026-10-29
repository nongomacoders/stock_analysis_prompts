# Reading Brief: Pan African Resources (PAN) Section D009 — Group Production Summary

**Target Section**: Section D009 (Group Production Summary, physical pages 48, 49, 50).  
**Source Document**: `companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf` (`62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd`).  
**Artifact Lineage**: Generated deterministically from `build/report.sqlite` (extraction commit `9d33906`, reconciliation suite commit `c62115e`). All calculations executed by `tests_reconcile/reconcile_engine.py`.

---

### 1. Key Facts and Figures

- **Gold Produced (Total)**:
  - **FY26 Group Total**: 272,310 oz (+38.6% YoY vs FY25 196,527 oz).
    - Mining operations: Barberton Mines 71,997 oz (underground 65,233 oz; surface 2,428 oz; third-party buy-in 4,337 oz); Evander Mines 46,855 oz (underground 40,246 oz; third-party buy-in 6,609 oz); Total Mining operations 118,853 oz.
    - Surface operations: BTRP 12,932 oz (tailings 10,974 oz; buy-in 1,958 oz); Elikhulu 56,475 oz (tailings); MTR operation 51,927 oz (tailings 46,164 oz; buy-in 5,763 oz); Tennant Mines 32,124 oz (surface feedstock); Total Surface operations 153,458 oz.
    - Total operations: Barberton total 94,929 oz; Evander total 103,330 oz; MTR total 51,927 oz; Tennant total 32,124 oz.
  - **FY25 Group Total**: 196,527 oz.
    - Mining operations: Barberton Mines 68,549 oz (underground 65,895 oz; surface 2,654 oz); Evander Mines 27,829 oz (underground 26,748 oz; buy-in 1,081 oz); Total Mining operations 96,378 oz.
    - Surface operations: BTRP 15,224 oz (tailings); Elikhulu 52,606 oz (tailings); MTR operation 30,806 oz (tailings 25,043 oz); Tennant Mines 1,513 oz (surface feedstock); Total Surface operations 100,149 oz.
- **Gold Sold (Total)**:
  - FY26: 272,373 oz (Mining 117,198 oz; Surface 155,175 oz).
  - FY25: 196,926 oz (Mining 96,956 oz; Surface 99,970 oz).
- **Financial Performance (Group Level, p.50)**:
  - **Revenue**: FY26 ZAR 17,249.1m (+77.5% YoY vs FY25 ZAR 9,715.6m). Barberton segment ZAR 8,449.6m + Surface operations segment ZAR 8,799.5m = Group total ZAR 17,249.1m (exact tie). Tennant Australian revenue printed separately as A$195.3m (FY25: A$5.9m).
  - **Cost of Production**: FY26 ZAR 6,431.7m (+26.5% YoY vs FY25 ZAR 5,084.0m). Barberton segment ZAR 3,957.4m + Surface operations ZAR 2,474.3m = Group total ZAR 6,431.7m (exact tie).
  - **Adjusted EBITDA**: FY26 US$663.1m (+169.8% YoY vs FY25 US$245.8m).
  - **Capital Expenditure**: FY26 US$214.9m (+31.4% YoY vs FY25 US$163.6m). Leaf segments sum: 37.5 + 49.8 + 2.6 + 21.1 + 32.6 + 71.3 = 214.9 US$m (exact tie).
- **Unit Costs & Realised Gold Prices (Group, p.49)**:
  - **Average Realised Price**: FY26 US$4,235/oz (FY25: US$2,735/oz); South African operations average ZAR 2,308,329/kg (FY25: ZAR 1,595,761/kg); Tennant Australian operations average A$195,501/kg (FY25: A$162,171/kg).
  - **Cash Cost**: FY26 US$1,600/oz (FY25: US$1,426/oz); ZAR 860,706/kg (FY25: ZAR 835,034/kg).
  - **AISC**: FY26 US$1,867/oz (FY25: US$1,600/oz); ZAR 985,551/kg (FY25: ZAR 934,517/kg).
  - **AISC (excl. buy-in)**: FY26 US$1,798/oz (FY25: US$1,599/oz).
  - **All-in Cost**: FY26 US$2,576/oz (FY25: US$2,383/oz); ZAR 1,271,855/kg (FY25: ZAR 1,287,842/kg).

---

### 2. Footnotes, Qualifications and Reconciliations

Deterministic execution of 526 arithmetic checks against the extraction database surfaced 68 mismatches, recorded as data in `conflicts` and evaluated on dedicated hypothesis branches without replacing any printed source figure:

1. **FY26 Barberton Total Operations Δ10,000 oz Gap (`Q-1f48aa6d4b884f09`)**:
   - Printed Total Operations Barberton (p.49 col9) is 94,929 oz.
   - Sum of printed components is Mining 71,997 oz (col0) + BTRP surface 12,932 oz (col3) = 84,929 oz (gap of +10,000 oz).
   - The leaf-column operations sum across segments is 94,929 + 103,330 + 51,927 + 32,124 = 282,310 oz, which exceeds printed Group total (272,310 oz) by the exact same 10,000 oz.
   - *Hypothesis evaluation*: Substituting 84,929 oz makes the operations sum tie printed Group total (272,310 oz) exactly. However, under Covenant 1 this is preserved as **conditional agreement only**; printed 94,929 oz remains in the database and the ledger question remains **open**.

2. **FY25 MTR Leaf vs Total Operations Δ5,763 oz Gap (`Q-3e8730dbd1994205`)**:
   - Printed FY25 MTR leaf tailings gold produced is 25,043 oz (p.48 col6), but MTR Total Operations prints as 30,806 oz (col11), a gap of 5,763 oz.
   - In FY26, MTR third-party buy-in feedstock is printed as 5,763 oz (col6 and col11), while in FY25 buy-in prints as nil (`–`).
   - *Hypothesis evaluation*: Adding 25,043 + 5,763 = 30,806 oz balances Total Operations, and component surface tailings (15,224 + 52,606 + 25,043 = 92,873) + 5,763 = 98,636 oz balances the printed surface tailings total. However, company text does not prove whether FY25 experienced 5,763 oz of unlabelled buy-in or if FY26 buy-in was retroactively misprinted. Per reviewed corrections, this question remains **open**.

3. **FY25 Group Gold Produced Reconciles via Disjoint Build (196,527 oz vs 197,608 oz)**:
   - A naive sum of printed leaf rows using the printed Group Underground column (93,724 oz) yields 197,608 oz (+1,081 oz above printed Group total 196,527 oz).
   - Reconciled via disjoint leaf decomposition: 92,643 (underground mining total) + 2,654 (surface mining) + 98,636 (surface tailings total) + 1,081 (buy-in) + 1,513 (Tennant surface feedstock) = **196,527 oz** (exact tie).
   - Proves that the printed Group Underground column (93,724 oz) embeds the 1,081 oz Evander buy-in (92,643 + 1,081 = 93,724), explaining the double-count in naive addition.

4. **Adjusted EBITDA FY26 Leaf-Sum (0.1 US$m Mismatch)**:
   - Sum of 6 leaf segments: 142.4 (Barberton) + 120.9 (Evander) + 29.4 (BTRP) + 171.4 (Elikhulu) + 155.9 (MTR) + 43.0 (Tennant) = 663.0 US$m vs printed Group Total 663.1 US$m. Recorded as a literal 0.1 mismatch rather than casually dismissed.

5. **Elikhulu FY25 All-in Cost Typography Anomaly (`Q-f1a4ce3647724ed9`)**:
   - Printed as ZAR 68,843/kg vs FY26 ZAR 853,597/kg. Cross-currency conversion at 18.17 US$/ZAR and 1,172 US$/oz implies ~684,658 ZAR/kg, indicating an omitted internal digit in the source printing.

6. **Tennant Operations Multi-Currency Consistency (`Q-ced8d2566db6459c`, `Q-c5e1b41b1cfe4dfb`)**:
   - FY25 Tennant all-in cost: printed 1,584,835 A$/kg ties 32,041 US$/oz at 1.54 US$/A$ within 0.10% relative deviation, driven by the tiny 1,179 oz sales base during commissioning.
   - Tennant revenue of A$195.3m (FY26) and A$5.9m (FY25) is presented in Australian Dollars on p.50, while Group Revenue is presented in ZAR (17,249.1m); whether Tennant is fully converted and consolidated into Group ZAR revenue requires verification in the group income statement (`Pending: S006/p.52`).

---

### 3. Questions Answered and Next Evidence

- `Q-1f48aa6d4b884f09` [medium]: **Partial**. Proved that FY25 group total (196,527 oz) ties the disjoint build (92,643 + 2,654 + 98,636 + 1,081 + 1,513), while FY26 operations sum ties 272,310 oz conditionally when substituting 84,929 oz. Causal origin of the 10,000 oz Barberton discrepancy remains open pending operational commentary (`Pending: S003/p.12`).
- `Q-e8c872e6edc94d18` [medium]: **Resolved** (arithmetic demonstrated). FY25 Evander Total (27,829 oz) comprises underground (26,748 oz) + third-party buy-in (1,081 oz). This same 1,081 oz is embedded in the Group underground column (92,643 + 1,081 = 93,724 oz).
- `Q-3e8730dbd1994205` [medium]: **Partial**. Arithmetic consistency proved (25,043 + 5,763 = 30,806 oz, matching FY26 buy-in 5,763 oz and balancing tailings total 98,636 oz). Kept open because source text does not explicitly confirm whether FY25 experienced unlabelled buy-in.
- `Q-f1a4ce3647724ed9` [medium]: **Partial**. Order-of-magnitude anomaly confirmed (68,843 vs implied ~684,658 ZAR/kg). Awaiting cost-schedule disclosure in notes (`Pending: S008/p.55`).
- `Q-ced8d2566db6459c` [low]: **Resolved**. Internal multi-currency consistency verified (1,584,835 A$/kg ties 32,041 US$/oz within 0.10%). Extreme FY25 level explained by division of initial operating costs over commissioning base of 1,179 oz.
- `Q-c1e6100f7a674873` [high]: **Open**. APM definitions for AISC and all-in cost (specifically treatment of buy-in feedstock and sustaining capital) require verification against APM disclosure (`Pending: S010/p.62`).
- `Q-a0b503d7ac044eee` [high]: **Open**. Reconciliation of per-oz costs to ZARm production costs at average exchange rates (16.90 and 18.17) requires full segmental note tie-up (`Pending: S006/p.52`).
- `Q-c5e1b41b1cfe4dfb` [medium]: **Open**. Consolidation of Tennant Australian revenue into Group ZAR revenue pending Group Statement of Comprehensive Income (`Pending: S006/p.52`).

**Next Evidence**: Section S003 / physical p.12 (Operational reviews) and Section S006 / physical p.52 (Financial statements).

---

### 4. Updated Open Questions Ledger

```markdown
- **Q-1f48aa6d4b884f09** [medium] (origin: trial_import): Reconcile FY26 Barberton Total Operations Gold produced (94,929 oz) with component sum (71,997 + 12,932 = 84,929 oz). Verify whether 10,000 oz represents an unlisted surface source or a printed column conflict. Target: S003, physical p.12.
- **Q-3e8730dbd1994205** [medium] (origin: trial_import): Clarify whether FY25 MTR Total Operations (30,806 oz vs leaf 25,043 oz) includes 5,763 oz of unlabelled third-party buy-in feedstock, matching FY26 buy-in (5,763 oz). Target: S003, physical p.14.
- **Q-f1a4ce3647724ed9** [medium] (origin: trial_import): Explain FY25 Elikhulu all-in cost printed as 68,843 ZAR/kg vs implied ~684,658 ZAR/kg and FY26 853,597 ZAR/kg. Target: S008, physical p.55.
- **Q-c1e6100f7a674873** [high] (origin: trial_import): Provide APM definitions used in D009: AISC, all-in cost, AISC excluding third-party buy-in feedstock, and Adjusted EBITDA. Target: S010, physical p.62.
- **Q-a0b503d7ac044eee** [high] (origin: trial_import): Reconcile per-oz cost metrics to p.50 ZARm production cost lines at 16.90 US$/ZAR (FY26) and 18.17 US$/ZAR (FY25). Target: S006, physical p.52.
- **Q-c5e1b41b1cfe4dfb** [medium] (origin: trial_import): Verify whether Tennant revenue (A$195.3m FY26; A$5.9m FY25) is consolidated into Group ZAR Revenue (17,249.1m) and at what exchange rate. Target: S006, physical p.52.
```
