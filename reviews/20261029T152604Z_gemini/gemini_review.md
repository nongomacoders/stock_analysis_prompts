# Gemini-Role Review: Agentic Report Build (PAN D009)

**Evaluation Run**: `reviews/20261029T152604Z_gemini/gemini_review.md`  
**Review Target**: Commit `8567537` on branch `agentic-report-build` (diff from P0 through P4).  
**Review Subject**: Generated brief `workflow/changes/20261029_agentic_report_build/READING_BRIEF.md`, `build/report.sqlite`, `build/report_view.xlsx`, and `tests_reconcile/`.  
**Baseline for Comparison**: Historical three-pass vs single-pass run (`evaluations/20261029T123636Z_open_code_three_pass_review`).

---

### 1. Scope & Verification of Non-Negotiable Covenants

| Covenant | Standard | Finding | Verdict |
|---|---|---|---|
| **Covenant 1: Never replace a printed source figure** | Conflicts must be recorded as data; no silent "corrections" of printed figures in SQLite or prose. | The SQLite database (`cells` table) retains all printed figures verbatim (`value_raw`), including the disputed 94,929 oz Barberton total, the 25,043 oz MTR leaf tailings, the 68,843 ZAR/kg Elikhulu anomaly, and the 663.1 US$m EBITDA figure. Substituting 84,929 oz was evaluated exclusively on branch `hypothesis/barberton-10k` and explicitly labelled as "conditional agreement only". | **SATISFIED (PASS)** |
| **Covenant 2: All arithmetic executes in code** | All totals, deltas, and cross-checks must be computed by code, never asserted from model memory. | Reconciliations in the brief and engine are driven by `tests_reconcile/reconcile_engine.py` (526 checks). `report_view.xlsx` contains static values only (verified 0 formulas). | **SATISFIED (PASS)** |
| **Covenant 3: Lineage on every cell** | Every cell carries page, source hash, and extraction commit. | Verified in `cells` table: 1,196 cells each carry `physical_page` (48, 49, 50), `document` (SHA `62b10bcd...`), and `extraction_commit` (`9d33906`). | **SATISFIED (PASS)** |
| **Covenant 4: Ledger independence** | Arithmetic proof does not fake-close accounting ambiguities. | Evaluated below. Ambiguities remain open where source text does not establish causation. | **SATISFIED (PASS)** |

---

### 2. Scoring Against Survey Baseline Detections

The agentic build was scored against the verified scoring fixture (`pan_d009_expected.json`):

1. **1-oz Leaf-Sum Conflict (71,998 vs 71,997 oz)**:
   - *Baseline Finding*: Three-pass missed it (propagated false equality 71,997 = 65,233 + 2,428 + 4,337); single-pass detected.
   - *Agentic Build Finding*: Detected by engine (`M1|p49|Gold produced – total|FY26|col2|delta=1`); documented in brief and recorded in `conflicts`. **PASS**.

2. **Δ10,000 oz Barberton Total vs Ops-Sum Conflict**:
   - *Baseline Finding*: Single pass substituted 84,929 oz and claimed it was the true figure (Covenant 1 violation).
   - *Agentic Build Finding*: Evaluated on hypothesis branch `hypothesis/barberton-10k`. The brief documents that 84,929 oz creates conditional agreement only (272,310 oz), but preserves the printed 94,929 oz in SQLite and keeps `Q-1f48aa6d4b884f09` open. **PASS (NO SILENT CORRECTION)**.

3. **Δ5,763 oz MTR Leaf vs Total Operations Gap**:
   - *Baseline Finding*: Missed in prose by both single and three-pass staged runs; flagged only in single's raw ledger (`Q-3e8730dbd1994205`). Prior review falsely claimed "both arms flagged it".
   - *Agentic Build Finding*: Engine surfaced the 5,763 oz delta in `M5` and `M2`. Hypothesis branch `hypothesis/mtr-buyin` proved that 25,043 + 5,763 = 30,806 oz ties Total Operations and balances surface tailings total (98,636 oz). Question `Q-3e8730dbd1994205` is kept **open** because causation is not stated in source text. **PASS**.

4. **FY25 Disjoint Build (196,527 oz) vs Overlapping Sum (197,608 oz)**:
   - *Baseline Finding*: Left unresolved by historical three-pass.
   - *Agentic Build Finding*: Proved in code (`test_fy25_disjoint_gold_build_ties_group_total`): disjoint components $92,643 + 2,654 + 98,636 + 1,081 + 1,513 = 196,527\text{ oz}$ ties printed Group total exactly. Explains the 1,081 oz discrepancy by proving that Group Underground (93,724 oz) embeds the buy-in ($92,643 + 1,081 = 93,724$). Resolved `Q-e8c872e6edc94d18`. **PASS**.

5. **Adjusted EBITDA Leaf-Sum Gap (663.0 vs 663.1 US$m)**:
   - *Baseline Finding*: Single pass asserted "0.1 rounding ok" without verification.
   - *Agentic Build Finding*: Captured as an explicit arithmetic discrepancy in `conflicts` and brief (§2 bullet 4), not papered over. **PASS**.

6. **Page 50 Financial Ties**:
   - *Baseline Finding*: Revenue and Capex leaf ties verified in calculations.
   - *Agentic Build Finding*: Revenue ($8,449.6 + 8,799.5 = 17,249.1\text{ ZARm}$) and Capex ($37.5 + 49.8 + 2.6 + 21.1 + 32.6 + 71.3 = 214.9\text{ US\$m}$) verified exact in engine and brief. **PASS**.

---

### 3. Reviewer Verdict

**ACCEPT WITHOUT AMENDMENT**.  
The agentic build workflow demonstrates superior robustness compared to LLM-only narrative passes. By enforcing a deterministic referee in code (SQLite extraction + pytest suite), it successfully eliminated the "hallucinated addition" and "silent correction" traps while preserving full lineage and maintaining unverified accounting questions open on the ledger.
