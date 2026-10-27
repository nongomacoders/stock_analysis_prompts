# Stock Evaluation & Valuation Output Protocol Specification

This document is the authoritative operating guide for the assistant whenever instructed to **evaluate** or **rerun** any company valuation note across the JSE coverage universe.

---

## 1. Operating Protocol & Trigger Recognition

Whenever the user prompts:
- `"evaluate <TICKER>"` (e.g. `"evaluate PAN"`, `"evaluate ORN"`, `"evaluate LEW"`)
- `"evaluate <TICKER> <PERIOD>"` (e.g. `"evaluate SPP 1H26"`)
- `"rerun <TICKER>"` / `"ok rerun"` / `"yes"` (following an evaluation with flags or model updates)

The assistant must execute the automated valuation pipeline using `evaluate_stock.py` rather than manually improvising analysis steps.

### CLI Execution Commands

1. **Initial Evaluation / Audit**:
   ```powershell
   .venv\Scripts\python.exe evaluate_stock.py <TICKER>
   ```
   *(Optionally specify `--period <PERIOD>` if evaluating an interim or specific historical period, e.g. `--period 1H26`)*

2. **Autonomous Rerun (Stage 2 Valuation Refresh)**:
   ```powershell
   .venv\Scripts\python.exe evaluate_stock.py <TICKER> --rerun
   ```
   *The `--rerun` command automatically aggregates the Stage 1 audit findings, source PDFs, and SENS notices into a multi-document dossier, queries DeepSeek Flash, sanitizes the markdown, updates `analysis.sqlite`, and archives source PDFs.*

---

## 2. Standardized User Output Structure

Whenever an evaluation or rerun is completed, the assistant **must** format its response into the following 5 distinct, structured sections:

```markdown
### <TICKER> — Institutional Valuation Scorecard (<PERIOD>)

**Audit Status:** [✓ `PASSED` | ⚠️ `WARNINGS_FOUND`] &nbsp;|&nbsp; **Sector:** `<SECTOR>` &nbsp;|&nbsp; **Dynamic Rating:** **`<DYNAMIC_RATING>`**

| Metric | Valuation Determination | Live Market Comparison & Basis |
| :--- | :---: | :--- |
| **Live JSE Price (`<TICKER>.JO`)** | **RXX.XX** | Sourced via live market data feed |
| **Note Reference Price** | RXX.XX | Baseline reference price in valuation note |
| **12-Month Target Price** | **RXX.XX** | Institutional valuation target |
| **Live Implied Upside** | **+XX.X%** | Relative to live price RXX.XX |
| **Forward Dividend Yield** | X.X% | 12-month forward cash distribution yield |
| **12-Month Expected TSR** | **+XX.X%** | Capital upside + forward dividend yield |
| **Recommendation** | **`<DYNAMIC_RATING>`** | Note static: `<STATIC_RATING>` (Dynamic Bands: `<DYNAMIC_RATING>`) |
| **Dynamic Rating Bands** | Strong Buy ≤ RXX.XX \| Buy ≤ RXX.XX \| Hold ≤ RXX.XX \| Sell ≤ RXX.XX \| Strong Sell > RXX.XX | Strictly monotonic ZAR thresholds |

---

#### Forensic Audit Checks
| Check Code | Check Description | Result | Details / Observations |
| :--- | :--- | :---: | :--- |
| **`CHK-PRICE-SYNC`** | Market Price & Upside Alignment | **[✓ PASS | ⚠️ FLAG]** | Detailed observation or price delta |
| **`CHK-BANDS-MONO`** | Rating Bands Monotonicity | **[✓ PASS | ⚠️ FLAG]** | Strict monotonicity check results |
| **`CHK-SOTP-MATH`** | SOTP Vertical Arithmetic & Sign Integrity | **[✓ PASS | ⚠️ FLAG]** | Net cash/debt signs and summation check |
| **`CHK-GUARDRAILS`** | Active Sector Guardrails Compliance | **[✓ PASS | ⚠️ FLAG]** | Compliance with sector-specific accounting rules |
| **`CHK-TEXT-CLEAN`** | LLM Stutter & Format Cleanliness | **[✓ PASS | ⚠️ FLAG]** | Scan for token repetition, <br>, <span> tags |

---

### Core Investment Thesis & Valuation Drivers
[Provide 2 to 3 substantive, quantitative paragraphs summarizing the asset's current operational state, key valuation drivers (e.g. DCF parameters, multiples, cost structures), and the primary structural headwinds and tailwinds.]

---

### Valuation Errors Found & Analytical Lessons Learned
[MANDATORY: Explicitly detail all errors, discrepancies, or misleading accounting treatments found in the valuation, and the critical analytical lessons learned.]

#### 1. Errors Found in the Valuation / Model:
* **[Error Name / Category]**: Detail the exact misstatement, omission, or distortion (e.g. stale reference prices, by-product AISC distortion, omitted dilution overhang, non-standard APM operating margins, hidden credit arrears, SOTP net cash sign flip).

#### 2. Analytical Lessons Learned:
* **[Lesson Name / Category]**: The fundamental, institutional takeaway for future modeling (e.g. always separate starter pits from LOM by-product credits, verify 100% parent debt guarantees against minority equity, audit 'satisfactory paid' credit books for hidden overdue instalments).

#### 3. Proposed New Guardrails (If Applicable):
* If a new repeatable pitfall is identified that is not yet in `sector_guardrails`, draft the proposed rule:
  - **Rule Code**: `<SECTOR>-<DESCRIPTOR>`
  - **Sector**: `<SECTOR>` (or `all`)
  - **Title**: `<DESCRIPTIVE_TITLE>`
  - **Rule Text**: `<EXPLICIT_MODELING_MANDATE>`

---

### Actionable Recommendation & Decision Gate
* **Current Dynamic Recommendation**: **`<RATING>`** (e.g. `BUY`, `HOLD`, `SELL`, `STRONG BUY`, `STRONG SELL`).
* **Rerun Action Required?**:
  - State clearly whether a rerun is recommended (e.g. if market price moved >10%, rating bands are broken, HTML tags exist, or financing terms changed) or confirm that the current valuation is solid and no rerun is needed.
* **Guardrail Database Codification Gate**:
  - If a new guardrail was formulated above, explicitly prompt the user:
    > *"Would you like me to codify the newly discovered guardrail (`<RULE_CODE>`) into the `sector_guardrails` database to permanently enforce this standard across all future valuations?"*
```

---

## 3. Mandatory Checklist for "Errors Found & Lessons Learned"

Whenever a new valuation is received or evaluated, the assistant must probe for and document sector-specific traps in the **Valuation Errors Found & Analytical Lessons Learned** section:

### 1. Mining Sector Checklist (`MINING`)
- **By-Product AISC Trap**: Did the model use a consolidated LOM headline AISC (subsidized by zinc, silver, or PGM by-products) to value a starter pit or phase with copper/gold-only ore?
- **Reserve vs. Inferred Deficit**: Does the LOM production schedule rely on Inferred Resources? If so, has an appropriate risk haircut (25–50%) or reserve conversion delay been applied?
- **Parent Debt Guarantee vs. Look-Through Stake**: Does the parent company guarantee 100% of subsidiary debt while owning only a partial economic interest (e.g. 50–70%)?
- **Financing Facility Conditionality**: Is debt split into unconditional tranches vs. conditional tranches requiring syndication?
- **Equity Dilution Overhang**: Are there facility structuring fees, convertible options, or lender equity kickers that must be added to fully diluted shares?
- **Section 36 Tax Shields**: Has the 100% upfront capital redemption shield been modeled to protect initial mining profits from corporate tax?

### 2. Retail & Consumer Credit Checklist (`RETAIL`)
- **Non-Standard APM Margin Distortion**: Did management calculate operating margin by dividing group EBIT by *merchandise sales only* rather than *total statutory revenue*?
- **Hidden Arrears in Credit Books**: Are there overdue instalments concealed inside accounts labeled as "satisfactory paid"? What is the true contractual delinquency?
- **Cash Flow vs. Accounting Profit Drain**: Is working capital absorbing massive cash into customer credit (trade receivables) despite positive accounting EBITDA?
- **Retail Core Trading Loss**: Is an underlying physical retail business running a severe trading deficit while masked by credit insurance fees or unbundled subsidiaries?

### 3. Conglomerates & Food Retail Checklist
- **Subsidiary Multiple Mirage**: Is the market cap dominated by a single listed subsidiary (e.g. Boxer in Pick n Pay), obscuring persistent operating losses in the core retail network?
- **Turnaround Realism**: Has the share price rallied on sentiment ahead of measurable operational turnaround metrics?

### 4. Construction & Materials Checklist (`CONSTRUCTION`)
- **Contract Assets (Unbilled WIP) Cash Lock-Up**: Is IFRS 15 percentage-of-completion revenue outpacing actual cash billing and collections?
- **Retentions & Payment Delays**: Are municipal infrastructure retentions tying up liquidity?
- **IAS 37 Onerous Contracts**: Are loss-making legacy contracts adequately provisioned?

---

## 4. Post-Rerun Synchronization Protocol

Whenever `--rerun` is executed and a new valuation is produced, the assistant must complete the following continuity checklist before concluding the turn:

1. **Verify Scorecard Execution**:
   - Run `evaluate_stock.py <TICKER>` to verify that all 5 forensic audit checks pass cleanly (`CHK-PRICE-SYNC`, `CHK-BANDS-MONO`, `CHK-SOTP-MATH`, `CHK-GUARDRAILS`, `CHK-TEXT-CLEAN`).
2. **Synchronize SQLite Database**:
   - Ensure the new target price, reference price, recommendation, upside, dividend yield, TSR, and dynamic rating bands are saved in `documents/analysis.sqlite` in the `reports` table.
3. **Archive Source PDFs**:
   - Verify that processed source PDFs from `companies/<SECTOR>/<TICKER>/sources/` are moved to `completed/<PERIOD>/`.
4. **Update Integration Tests**:
   - If tests in `tests/test_portfolio_valuation.py` assert against specific values in the company valuation note on disk, update the test assertions to reflect the refreshed values.
5. **Run PyTest Suite**:
   - Execute `.venv\Scripts\python.exe -m pytest tests -q -p no:cacheprovider --basetemp=tmp/<unique-task>`.
   - Ensure all 133+ tests pass (100% exit code 0).
   - Clean up the temporary test folder (`tmp/<unique-task>`) immediately.
6. **Update `workflow/STATE.md`**:
   - Add a bullet under `## Completed` detailing the refreshed valuation metrics, recommendation, live price basis, and source archival.
