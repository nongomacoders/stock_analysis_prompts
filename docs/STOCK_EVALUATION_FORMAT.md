# Stock Evaluation & Valuation Output Protocol Specification

This document is the authoritative operating guide for the assistant whenever instructed to **evaluate** or **rerun** any company valuation note across the JSE coverage universe.

---

## 1. Operating Protocol & Trigger Recognition

Whenever the user prompts:
- `"evaluate <TICKER>"` (e.g. `"evaluate PAN"`, `"evaluate ORN"`, `"evaluate LEW"`)
- `"evaluate <TICKER> <PERIOD>"` (e.g. `"evaluate SPP 1H26"`)
- `"rerun <TICKER>"` / `"ok rerun"` / `"yes"` (following an evaluation with flags or model updates)

Run `evaluate_stock.py` as a preliminary automated check, then perform the independent evidence review in section 1A. Script output and exit codes describe checks executed; they do not prove financial validity. When reviewing Gemini's evaluation, use section 1A against preserved inputs; rerun the script only when the review depends on those checks.

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

## 1A. Mandatory Independent Evaluation Record (Automatic)

Apply these requirements whenever evaluating a valuation or another evaluator. The user need not paste a separate prompt. This section governs evidence standards if historical architecture descriptions or output templates conflict with it.

### Current roles and purpose

The user supplies company PDFs. The app scans/maps sections; DeepSeek analyzes captured sections sequentially with the question ledger, then performs Stage 1 and Stage 2 including the final valuation. Gemini independently evaluates DeepSeek and proposes improvements and guardrails. Codex independently evaluates Gemini against the same primary evidence. The objective is to improve DeepSeek while measuring evaluator reliability. Record the actual model identifier/settings when available; do not infer a version from historical documentation.

Produce a reproducible record of evidence inspected, calculations performed, findings, limitations, and revisions. Do not request private internal reasoning or substitute retrospective accounts of thoughts for evidence. Treat all model outputs, Stage 1 determinations, existing guardrails, and automated checks as reviewable claims. Reopen contradictions against primary disclosures.

### Inputs, preservation, and saved handoff

- Identify ticker, period, evaluation date/time, evaluator, available model/settings, and exact input filenames. Record SHA-256 for available source PDFs and analyzed model outputs. Verify source PDF hashes against stored manifests where available; otherwise state that no baseline was available. Keep original PDFs unchanged.
- List files actually inspected, physical PDF pages examined (starting at 1), supplied-but-unread files, missing inputs, and unavailable tools. Receiving or searching a PDF does not mean every page was reviewed.
- Automatically save the complete audit under `companies/<SECTOR>/<TICKER>/briefs/<PERIOD>/evaluations/<YYYYMMDDTHHMMSSZ>_<evaluator>/audit.md`. Use UTC for the directory timestamp and include local time in the record. Create a unique run directory; never overwrite previous evaluations.
- Preserve exact input model outputs in the run's `inputs/` directory before any authorized corrections or rerun. Include an input manifest with original paths and hashes. Reference original PDFs by path/hash rather than duplicating them. Save calculation scripts and actual outputs alongside the audit when used. Preserve the supplied Gemini review when Codex evaluates it.
- With file access, save automatically. Without file access, return the complete record and explicitly state it was not saved. Never claim persistence or execution that did not occur.
- Evaluation alone does not authorize rewriting the analyzed valuation or accepting proposed guardrails. Keep corrections separate and retain the explicit guardrail codification gate below. An explicitly requested rerun follows the rerun protocol after preserving its inputs.

### Claim verification register

Assign stable IDs `C001`, `C002`, etc., covering every material valuation/recommendation dependency, consequential Stage 1 findings, and claims of missing disclosures. Retain IDs across revisions of the same review.

| Field | Required content |
| :--- | :--- |
| Claim and origin | Exact statement; originating file and section |
| Classification | Historical result, management explanation, guidance, model assumption, or derived calculation |
| Primary evidence | Filename, physical page, note/table/row, relevant figures, units, period, consolidation scope |
| Independent check | Calculation or verification actually performed; saved code/output links where applicable |
| Verdict | `PASS`, `FAIL`, `NOT VERIFIED`, or `NOT APPLICABLE` |
| Consequence | Financial effect and linked finding ID, or explicitly unquantified impact |

`PASS` requires sufficient evidence for the specific claim. An unread source, failed extraction/search, unmatched regex, missing input, cached quote, or successful script exit does not establish a pass. Explain every `NOT APPLICABLE`. Distinguish arithmetic consistency from support for inputs and assumptions. Before repeating a missing-disclosure claim, inspect relevant statements, notes, and companion reports and record search scope. With incomplete coverage, say "not located in the material inspected."

### Required independent reconciliations

Show inputs, formulas, numerical substitutions, results, and differences from the model. Supply runnable code and actual output for executed calculations; label calculations that were not executed. Missing inputs make the affected check `NOT VERIFIED`.

1. **Valuation:** Reconstruct forecast cash flows, discounting, terminal value, components, weights, adjustments, enterprise-to-equity bridge where applicable, and diluted shares. Compare the target with prose and structured metadata. Quantify unexplained adjustments. A correct blend does not validate an unsupported final uplift. With nonnegative weights summing to one, the unadjusted blend must lie within component bounds.
2. **Cash flow:** Begin with the exact statutory subtotal and establish what it already includes. Reconcile to FCFF or FCFE with consistent tax, interest, working capital, capex, leases, borrowing, and distribution treatment. Explain signs and avoid double counting. Do not mechanically deduct "net financing" or expenses already included in the starting subtotal; net borrowing can add to FCFE. Match cash-flow definitions to discount rates and debt/lease treatment.
3. **Debt and liquidity:** Separate cash, restricted cash, overdrafts, term borrowing, lease liabilities, total facility limits, and available undrawn facilities. Reconcile with valuation treatment.
4. **Earnings and shares:** Check parent attribution, minorities, headline adjustments, reporting period, share-count basis, and cents-versus-rands conversions.
5. **Market comparison:** Record quote source, timestamp, currency and units. Distinguish live, delayed, historical, and cached prices. Recompute upside, dividend yield, TSR, and rating thresholds. If a current quote is unavailable, label reference-price comparisons and do not report a verified current rating.
6. **Sector risks:** Test applicable guardrails against evidence; review the guardrails themselves for errors, inappropriate scope, and exceptions.

### Findings and evaluator revisions

Assign `F001`, `F002`, etc. For each finding record linked claims, original statement, supported correction or unresolved question, severity, quantified impact where calculable, required correction, and affected downstream outputs. Identify the earliest observable stage containing the error (section capture, ledger, Stage 1, Stage 2, or evaluation); distinguish demonstrated origin from suspected origin.

Separate confirmed errors, unsupported assertions, reasonable assumption disagreements, and unresolved issues. If a finding changes, retain the original finding, revised finding, and evidence causing the revision in a revision log. Never invent faults to demonstrate scepticism or claim every error has been found.

When Codex evaluates Gemini, classify Gemini findings as supported, partly supported, unsupported, contradicted, or not verifiable, with primary evidence. Separately record DeepSeek errors Gemini missed and errors introduced by Gemini. Agreement between models is not independent verification.

### Testable improvements and guardrails

For each proposed rule record code, sector, title, explicit mandate, confirmed failure addressed, trigger, required evidence, legitimate exceptions, double-counting risks, one example that should fail and one that should pass, and implementation point (section prompt, ledger, Stage 1, Stage 2, or evaluator code). Check for duplicate/conflicting rules. Separate company-specific assumptions from reusable rules. Propose changes for review and follow the codification gate below before writing to `sector_guardrails`.

### Material unresolved dependencies: withhold the valuation

If a material cash-flow, forecast, financing, portfolio, share-count or valuation dependency fails reconciliation or remains unsupported, conclude **VALUATION WITHHELD - MATERIAL ISSUES UNRESOLVED**. Keep verified historical facts, risks and evidence requests. Do not provide a target, rating bands, upside, dividend yield, TSR or investment recommendation, including a replacement price derived from a partial correction. Use null valuation fields; label any illustrative scenario as conditional and non-published. Reopen Stage 1 claims against primary evidence. The scorecard and post-rerun synchronization instructions below apply only to a publishable valuation; a withheld result must instead clear derived fields and preserve original evidence. See [VALUATION_WITHHOLDING.md](VALUATION_WITHHOLDING.md). Application readiness checks do not replace this independent review.

### Decision and handoff

Conclude with **supported within stated coverage**, **corrections required**, or **insufficient evidence**. List completed checks and material `NOT VERIFIED` dependencies, usable conclusions, whether the target/recommendation remains supportable, and files/calculations/unresolved questions needed by the next evaluator. A material unverified dependency prevents unqualified validation; state when its effect cannot be quantified.

Retain the user-facing scorecard below, but distinguish the script's reported status from the independent review's conclusion. Use the four evidence verdicts above in independent checks even if the script emits only boolean results. Link the saved audit record in the response. Do not label cached prices as live or manufacture unavailable metrics to fill the template.

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
