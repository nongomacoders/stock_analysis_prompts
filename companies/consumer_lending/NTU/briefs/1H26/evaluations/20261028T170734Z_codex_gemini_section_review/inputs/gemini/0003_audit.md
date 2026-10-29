# Section reading prompt — paired pilot

Implemented one shared four-part task with conditional notes for8 sectors;existing ledger schema/source references retained. No PDF split changes,Stage1/2 reruns,production SQLite writes or new financial guardrails.

| Case | Old/new ledger valid | Old/new questions | Old/new seconds |
|---|---|---:|---:|
| ntu_portfolio | True/True | 5/3 | 12.72/11.27 |
| ntu_shared_page | False/True | 6/2 | 16.37/8.24 |
| pan_apm | True/True | 6/3 | 12.75/8.04 |
| pan_operations | True/True | 9/4 | 13.69/11.74 |

```json
{
  "old": {
    "proposed_questions": 26,
    "prompt_chars": 109642,
    "completion_tokens": 13655,
    "input_tokens": 31304,
    "elapsed_seconds": 55.522,
    "cached_tokens": 4254,
    "cost_usd": "0.0171685668",
    "valid_ledgers": 3
  },
  "new": {
    "proposed_questions": 12,
    "prompt_chars": 90892,
    "completion_tokens": 9165,
    "input_tokens": 26620,
    "elapsed_seconds": 39.28,
    "cached_tokens": 2178,
    "cost_usd": "0.0128405676",
    "valid_ledgers": 4
  }
}
```

All8 costs corroborated by generation metadata. TotalUSD0.0300091344. Full offline suite226 passed in104.57s,exit0. Initial targeted run52 passed/1 failed because a test loaded standalone sector templates;updated for shared assembly.

Decision: prompt simplification and basic operation supported within sample;financial correctness still requires review. Known revised-output error:wrong FV sign in NTU ledger (584 mathematically,not644);prose is correct. Inappropriate POCI staging question and unsupported interpretations remain. No model output corrected and no paid repair loop.

Coverage:NTU p13/p25;PAN p38–39/p48–50 selected extracted captures. Source PDFs hash-verified;no new PDF image review. No current price,forecast or valuation validation. Cache/order/provider-default limitations are in comparison.json. Original prompts/code preserved in inputs/driver_and_baseline;exact requests/outputs/receipts retained. Preliminary ledger checks are not financial validation.

## Findings

**F001 — SUPPORTED WITHIN SAMPLE:** All8 generations completed. Revised ledgers4/4 literal-validation passes versus3/4 old;old NTU shared-page quote nonliteral. This does not validate financial truth.

**F002 — CONFIRMED ERROR:** Revised NTU p13 prose correctly adds FV30,but its ledger answer writes702+28−116−30=644. Actual equation equals584,a60 difference. Correct sign gives644. Earliest observed in this section output;original retained,not repaired.

**F003 — UNSUPPORTED APPLICABILITY:** Revised NTU p13 warns against conventional staging then requests staging/coverage evidence for POCI. Conditional sector hints reduce rigid scope but do not reliably prevent irrelevant demands. Existing approved rules not changed.

**F004 — PARTLY SUPPORTED:** Both old and revised NTU p25 include currency-risk start and next-page dependency. Revised answer is shorter with fewer questions. No unique coverage improvement over this paired old answer can be claimed.

**F005 — UNSUPPORTED ASSERTION:** First-time comparative presentation does not itself prove a newly constructed/restated comparative or a provisioning-method change. Both NTU p25 answers overinterpret those points;methodology remains unverified.

**F006 — NOT VERIFIED:** Revised PAN operational answer flags shifted extraction columns and keeps mappings provisional. Cell/asset attribution and its prior-year component residual require original-table inspection. Prompt changes do not repair extraction layout.

## Unverified dependencies

Semantic question closure,all table-cell attribution,full-report completeness,other sectors/companies,forecast/DCF and downstream Stage1/2 outcomes NOT VERIFIED. No target/recommendation created. No new sector_guardrails proposed or codified;this is a prompt pilot. Raw model answers remain review subjects.

Tool/accounting revision:normalized inherited receipt fields from exact saved request controls;original receipts preserved.
