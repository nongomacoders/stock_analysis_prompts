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