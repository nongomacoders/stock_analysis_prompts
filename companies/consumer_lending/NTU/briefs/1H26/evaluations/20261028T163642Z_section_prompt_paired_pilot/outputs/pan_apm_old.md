### 1. Answers to Stored Questions for This Section
*(No stored questions were supplied — first capture. Section omitted per workflow rule.)*

### 2. Footnote & Qualification Deep-Dive
No footnote markers (`[^1]`, `*`) appear in the supplied D008.1 evidence. However, several embedded qualifications materially change interpretation of the APM tables and must be flagged:

- **"99.7% of the Group's revenue" is gold** `[D008.1, physical PDF p. 38]`. This is the stated justification for treating per-unit costs as comparable across operations. It implies ~0.3% non-gold revenue (by-product credits) that is *deducted* from operating costs in the AISC definition (see below). The 0.3% figure is a forecast input and a check item — it must reconcile to segment revenue in D006.2.
- **AISC definition explicitly deducts by-product revenue** `[D008.1, physical PDF p. 39]`: "The value of by-product revenue is deducted from operating costs as it effectively reduces the cost of gold production." This means AISC is *net* of by-product credits; any change in by-product (non-gold) revenue flows straight into AISC/oz. Must verify the by-product credit quantum in D006.2/D009.
- **AISC excludes "non-gold operations"** `[D008.1, physical PDF p. 38]` (sustaining and development capital "excluding non-gold operations"). So the AISC cost base is gold-only; non-gold capex sits outside AISC and must be picked up separately in the capex forecast (D006.5/D006.7).
- **Lower-cost vs higher-cost split is a management construct, not an IFRS line** `[D008.1, physical PDF p. 39]`. The split (FY26: 247,219 oz lower-cost @ US$1,702/oz vs 25,154 oz higher-cost @ US$3,487/oz) is not defined by mine in this section. The identity of which operations sit in each bucket, and whether the classification is stable year-on-year, is unverified and critical for forecasting blended AISC.
- **Free cash flow definition includes a non-standard deduction**: "Less capital expenditure funded through permitted indebtedness" `[D008.1, physical PDF p. 39]`. This is an unusual adjustment — capex funded by debt is deducted from FCF, which will make reported FCF lower than a conventional FCF and is a reconciliation trap. Must verify the amount and which facilities are "permitted indebtedness" in D006.
- **Net (cash)/debt and net senior debt both exclude IFRS 9 adjustments, restricted cash and "financial liabilities"** `[D008.1, physical PDF p. 39]`. The exclusion of "financial liabilities" from net debt is broad and undefined here; the magnitude of excluded financial liabilities must be quantified in D006 (likely D006.8/D006.9 borrowings notes) to reconcile to the statement of financial position (D005).
- **Headline earnings per SAICA Circular 1/2023** `[D008.1, physical PDF p. 39]` — the adjustment list (disposal of PPE, impairments, bargain purchase, tax effect) is standard, but the actual reconciling items and their tax effects are not shown here; they must be traced to the HEPS reconciliation (likely D006.4 income tax / D006.11).

### 3. New Questions to Check in Future Sections

| Q# | Priority | Target section (from Report Map) | Claim, anomaly, or footnote trigger `[D00X, p. Y]` | Specific verification instruction (what exact figure/note/table to check in the target section) | Why it matters for the forecast |
| --- | --- | --- | --- | --- | --- |
| Q1 | High | D006.2 (Note 3 Segment Analysis) | Gold = 99.7% of revenue; AISC deducts by-product revenue `[D008.1, p. 38–39]` | Reconcile segment revenue to confirm the ~0.3% non-gold/by-product revenue; quantify by-product credits deducted from AISC. | By-product credits directly reduce AISC/oz; a shift changes unit-cost forecast. |
| Q2 | High | D006.2 / D009 | Lower-cost (247,219 oz @ $1,702) vs higher-cost (25,154 oz @ $3,487) split undefined by mine `[D008.1, p. 39]` | Identify which operations are in each bucket and confirm the oz/cost allocation ties to segment and production summary. | Blended AISC forecast depends on the mine-level cost mix and any reclassification. |
| Q3 | High | D006 (borrowings notes, D006.8/D006.9) | Net debt excludes "financial liabilities", restricted cash, IFRS 9 adjustments `[D008.1, p. 39]` | Quantify each excluded item and reconcile net (cash)/debt and net senior debt to statement of financial position (D005). | Determines true leverage and interest forecast; excluded liabilities could understate debt. |
| Q4 | Medium | D006 (cash flow / capex notes) | FCF deducts "capital expenditure funded through permitted indebtedness" `[D008.1, p. 39]` | Identify the amount and the facilities classed as permitted indebtedness; confirm the FCF reconciliation. | Changes FCF vs conventional definition; affects debt-service and dividend capacity view. |
| Q5 | Medium | D006.4 / D006.11 | Headline earnings adjustments per SAICA Circular 1/2023 `[D008.1, p. 39]` | Trace actual reconciling items (disposals, impairments, bargain purchase, tax effect) and confirm HEPS reconciliation. | Needed to forecast normalised earnings vs IFRS PAT. |
| Q6 | Low | D006.5 / D006.7 | AISC excludes non-gold operations' sustaining/development capex `[D008.1, p. 38]` | Identify non-gold capex excluded from AISC and add back into total capex forecast. | Prevents understating group capex. |

### 4. Updated Open Questions Ledger
```json
{"ledger_version": 1, "updates": [], "new_questions": [
  {"question": "Reconcile the ~0.3% non-gold revenue (gold = 99.7% of Group revenue) and quantify by-product revenue deducted from operating costs in the AISC definition.", "priority": "high", "target_document": "Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf", "target_section": "D006.2", "evidence_required": "Segment revenue split (gold vs by-product/non-gold) for FY26 and FY25 in US$ and %, plus the by-product credit amount deducted in the AISC reconciliation.", "closure_condition": "Segment revenue confirms gold share and the by-product credit quantum is identified and ties to the AISC build; benign explanation accepted if immaterial."},
  {"question": "Identify which operations comprise the lower-cost (247,219 oz @ US$1,702/oz) and higher-cost (25,154 oz @ US$3,487/oz) AISC buckets and confirm the allocation ties to segment and production data.", "priority": "high", "target_document": "Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf", "target_section": "D006.2", "evidence_required": "Mine-level AISC and oz sold for FY26/FY25 reconciling to the 247,219/25,154 oz and US$420.686m/US$87.718m totals; note any reclassification between buckets.", "closure_condition": "Mine-level costs sum to the bucket totals and the bucket membership is stated; forecast consequence for blended AISC noted."},
  {"question": "Quantify the items excluded from net (cash)/debt and net senior debt (IFRS 9 adjustments, restricted cash, financial liabilities) and reconcile to the statement of financial position.", "priority": "high", "target_document": "Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf", "target_section": "D006.8", "evidence_required": "Borrowings/lease note figures for each excluded item in US$, and a reconciliation of net debt and net senior debt to D005 statement of financial position balances.", "closure_condition": "Each exclusion is quantified and the reconciliation to the primary statement balances; benign explanation accepted if immaterial."},
  {"question": "Identify the amount of capital expenditure funded through permitted indebtedness deducted in the free cash flow definition and the relevant facilities.", "priority": "medium", "target_document": "Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf", "target_section": "D006", "evidence_required": "Capex-funded-by-debt amount in US$ for FY26, the facility names, and the FCF reconciliation showing the deduction.", "closure_condition": "Amount and facility identified and FCF reconciliation ties; forecast consequence for FCF vs conventional definition stated."},
  {"question": "Trace the actual headline earnings reconciling items (disposal of PPE, impairments, bargain purchase, tax effect) per SAICA Circular 1/2023 and confirm the HEPS reconciliation.", "priority": "medium", "target_document": "Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf", "target_section": "D006.11", "evidence_required": "Itemised headline earnings adjustments with tax effects in US$ and the HEPS/basic EPS reconciliation for FY26 and FY25.", "closure_condition": "Each adjustment is quantified with tax effect and reconciles to HEPS; forecast consequence for normalised earnings noted."},
  {"question": "Identify non-gold operations' sustaining and development capex excluded from AISC and confirm it is captured in total group capex.", "priority": "low", "target_document": "Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf", "target_section": "D006.5", "evidence_required": "Non-gold capex amount in US$ excluded from AISC and its inclusion in the PPE/capex note totals.", "closure_condition": "Non-gold capex quantified and reconciled into total capex; benign explanation accepted if immaterial."}
]}
```

### 5. Baseline Forecast Inputs Captured Here
| Metric | FY26 | FY25 |
| --- | --- | --- |
| AISC — lower-cost ops (US$m) | 420.686 | 241.957 |
| AISC — higher-cost ops (US$m) | 87.718 | 73.111 |
| AISC — total Group (US$m) | 508.405 | 315.068 |
| Gold sold — lower-cost (oz) | 247,219 | 168,781 |
| Gold sold — higher-cost (oz) | 25,154 | 28,146 |
| Gold sold — total Group (oz) | 272,373 | 196,927 |
| AISC/oz — lower-cost (US$/oz) | 1,702 | 1,434 |
| AISC/oz — higher-cost (US$/oz) | 3,487 | 2,598 |
| AISC/oz — total Group (US$/oz) | 1,867 | 1,600 |
| Gold share of Group revenue | 99.7% | — |

### 6. Next Section to Capture
**D006.2 (Note 3 Segment Analysis)** — resolves Q1 and Q2 (by-product credits, gold revenue share, and mine-level AISC bucket allocation), and provides the segment data needed to anchor Q3–Q6.