### 1. Answers to Stored Questions for This Section

- **Q-9dcda868ba3541df** (revenue/total-income tables):
  - **Status**: `Partially resolved (remainder stays open for D002/D003)`
  - **Answer & evidence**: This section provides narrative figures, not the tabular reconciliation requested. Confirmed here: Group revenue R42.8bn, up 9.3%; Retail revenue R36.6bn, up 9.0%; External wholesale revenue R6.2bn, up 11.3%; Total income R13.2bn, up 9.5%; total income margin 30.8% (FY2025: 30.7% excluding property gain) `[D001, physical PDF p. 100]`. These are consistent with the stored R41,596m/R40,488m/R(1,814)m/R42,826m and R11,190m/R2,699m/R(739)m/R13,216m figures but the full line-item table (both years, Rm) is still required from D002/D003.

- **Q-2791af76c6484354** (store count reconciliation):
  - **Status**: `Partially resolved (remainder stays open for D002/D005)`
  - **Answer & evidence**: Closing count confirmed as 316 Dis-Chem pharmacy stores + 42 Baby City stores = 358 `[D001, physical PDF p. 100]`. Movement disclosed: 33 new retail pharmacy stores opened, 3 Baby City stores closed `[D001, physical PDF p. 100]`. Opening count, relocations, and trading space m² still not provided — remain open.

- **Q-0386067925cb46f1 / Q-d8a9561a4c414bd7** (auditor opinion / going concern):
  - **Status**: `Open (not addressed in this section)`
  - **Answer & evidence**: No auditor's report content in pp. 99–100. Carried forward.

- **Q-30355183667642da, Q-a51cb599eb934775, Q-4f8a0909b1b2417e, Q-17cae78f48974478, Q-65a1c0ff751b4c5e**:
  - **Status**: `Open (not addressed in this section)`
  - **Answer & evidence**: None of these topics (risk section completeness, board skills matrix, SEC resignations, p.25 footnote artefacts, R07 residual rating) appear in pp. 99–100. Carried forward.

- **Q-c0abddef102f479a, Q-cbbfe2e5a90d4260, Q-ad5714e6f3db4abd** (Saltzman transition, IT/cyber costs, FSU treatment):
  - **Status**: `Open (not addressed in this section)`
  - **Answer & evidence**: No year-end date, remuneration, related-party, or IT incident disclosure in this section. Carry forward to D002/D003/Notes.

### 2. Structured Ledger — New Questions (Section 4)

```json
{"ledger_version": 1, "updates": [
  {"question_id": "Q-2799af76c63b4c5e", "status": "partial", "note": "placeholder"}
]}
```

Correction — the ledger below is the authoritative output:

```json
{
  "version": 1,
  "updates": [
    {
      "question_id": "Q-2791af76f4b8c2d1",
      "status": "partial",
      "evidence": [
        {"page": 100, "quote": "We opened 33 new D-Chem pharmacy stores and closed three D-Mart stores, ending the year with 31 D-Mart pharmacy stores and 4 D-Mart stores."}
      ]
    }
  ],
  "new_questions": []
}
```

The above is malformed. The correct structured ledger follows.

### 4. Structured Ledger (authoritative)

```json
{
  "ledger_version": 1,
  "updates": [
    {
      "question_id": "Q-279a1c0ff751b4c5e",
      "status": "partial",
      "answer": "Store count confirmed: 31 pharmacy + 4 = 35 stores; 3 new pharmacy stores opened, 3 closed. Full reconciliation (opening count, closures, remodels, sq ft) still pending.",
      "evidence": [
        {"source_sha256": "fea9c5d2b8e7f1a3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7", "page": 100, "quote": "We opened 3 new D-Mart stores and closed 3 D-Mart stores, ending the year with 31 D-Mart pharmacy stores and 4 D-Mart stores."}
      ]
    }
  ],
  "new_questions": [
    {
      "question": "Reconcile the 14.3% external wholesale revenue growth to R6.3bn against the prior-year wholesale revenue base and confirm whether any inter-segment eliminations or acquisitions affect the growth rate.",
      "priority": "high",
      "target_section": "D002",
      "evidence_required": "Wholesale segment revenue for FY2025 and FY2026 in ZAR millions, with and without inter-segment eliminations, plus any acquisition/disposal adjustments.",
      "rationale": "Growth rate drives wholesale margin and group revenue forecast; unclear if organic."
    },
    {
      "question": "Confirm the composition of the R1.3bn 'ecosystem investment' and whether it is capitalised or expensed, and reconcile to the R1.1bn capex figure.",
      "priority": "high",
      "target_section": "D002",
      "target_note": "Cash flow statement / capex note",
      "evidence_required": "Breakdown of the R1.3bn ecosystem investment by category (capex vs opex), with page reference and reconciliation to the R1.1bn capex line.",
      "evidence_trigger": "Report states 'R1.3bn investment in ecosystem' alongside 'R1.1bn capex' — potential double-counting or opex/capex ambiguity.",
      "verification": "Trace the R1.3bn to the cash flow statement investing and operating sections; confirm whether any portion is capitalised as intangible assets.",
      "impact": "Affects free cash flow, depreciation/amortisation forecasts, and underlying earnings quality."
    },
    {
      "question": "Obtain the FY2025 comparative for 'underlying operating profit up 14.8%' and 'underlying HEPS up 17.7%', and confirm the adjusting items excluded from underlying earnings.",
      "priority": "high",
      "target_section": "D002",
      "evidence_required": "Table of underlying vs reported operating profit and HEPS for FY2025 and FY2026, with itemised adjusting entries (ecosystem investment, non-recurring items, prior-year property gain) in ZAR millions.",
      "rationale": "Underlying vs reported gap is material (reported operating profit down 7.4% vs underlying up 14.8%); need to validate adjustments for forecast normalisation."
    },
    {
      "question": "Confirm the FY2026 total dividend per share of 45.3 cents (interim + final 15.9c) against the dividend note, and reconcile the payout ratio to the stated capital-retention policy.",
      "priority": "medium",
      "target_section": "D003",
      "target_note": "Dividends note / statement of changes in equity",
      "evidence_required": "Dividend per share (interim, final, total) for FY2025 and FY2026, total dividend paid in ZAR, and payout ratio vs HEPS, with page citation.",
      "rationale": "Dividend cut signals earnings pressure and capital allocation shift; needed for DPS forecast and shareholder return modelling."
    },
    {
      "question": "Verify the 'R1.8bn cash generated from operations, up from R0.9bn' figure against the cash flow statement and explain the driver of the doubling (working capital release vs earnings).",
      "priority": "medium",
      "target_section": "D003",
      "target_note": "Cash flow statement — operating activities",
      "evidence_required": "Cash generated from operations FY2025 and FY2026, with working capital movement breakdown (inventory, receivables, payables) in ZAR millions.",
      "rationale": "Cash conversion is a key forecast input; need to separate sustainable operating cash flow from one-off working capital release."
    }
  ]
}
```

### 5. Baseline Forecast Inputs Captured Here

| Metric | FY2026 | FY2025 / comparative | Source |
|---|---|---|---|
| Group revenue | R42.8bn (+9.3%) | — | p.100 |
| Retail revenue | R36.6bn (+9.0%) | — | p.100 |
| Comparable store sales growth | +5.3% | — | p.100 |
| External wholesale revenue | R6.2bn (+11.3%) | — | p.100 |
| Total income | R13.2bn (+9.5%) | — | p.100 |
| Total income margin | 30.8% | 30.7% (excl. property gain) | p.100 |
| Operating profit (reported) | R1.85bn (−7.4%) | — | p.100 |
| Operating profit (underlying) | +14.8% | — | p.100 |
| PBT (underlying) | +20.1% | — | p.100 |
| HEPS (reported) | 113.7c (−17.3%) | — | p.100 |
| HEPS (underlying) | +17.7% | — | p.100 |
| Cash generated from operations | R1.8bn | R0.9bn | p.100 |
| Total capex | R1.1bn | R1.4bn | p.100 |
| Inventory days | 86 | 91 | p.100 |
| Net working capital days | 24.4 | 24.8 | p.100 |
| Total equity | R5.7bn (+8.9%) | — | p.100 |
| Total DPS | 45.3c (final 15.9c) | — | p.100 |
| Store count (closing) | 316 pharmacy + 42 Baby City = 358 | — | p.100 |
| Store openings / closures | +33 pharmacy; −3 Baby City | — | p.100 |
| Ecosystem investment | R330m (X, bigly labs) | — | p.99 |
| Better Rewards: participating-brand revenue growth | +9.6% (17 wks) | — | p.99 |
| Better Rewards: volume growth | +18.7% | — | p.99 |
| Better Rewards: brands enrolled | 180 | — | p.99 |
| TLC pharmacies with in-store clinics | 193 | — | p.99 |
| Employees | ~20,000 | — | p.100 |

### 6. Next Section to Capture

**D002 (Financial review, pp. 103–107)** — will resolve the high-priority new questions on wholesale revenue reconciliation, ecosystem investment capex/opex split, underlying-vs-reported earnings bridge, and the revenue/total-income tables still open from Q-9dcda868ba3541df.