# NTU 1H26 — default-thinking / standard-routing run

**Execution INCOMPLETE: Stage1 completed; full Stage2 exhausted its completion ceiling with no final answer.** No production valuation was replaced.

- Model: `deepseek/deepseek-v4.1-flash-1017`; reasoning controls omitted (catalog default enabled/high); no Nitro or speed/provider-priority override.
- First dispatch UTC: 2026-10-28T10:13:20.504898+00:00; execution ended UTC: 2026-10-28T10:33:15.864595+00:00.
- First dispatch to last accounting: **1195.33 seconds** (includes pilot/revision pauses, repairs and metadata lookup).
- Summed generation request elapsed: **823.17 seconds**; does not include all orchestration pauses.
- Recorded API cost: **USD 0.18930894**; calls missing cost: 0. Includes failed/truncated attempts and repairs.
- Calls: 15; completed generations: 11.
- Prompt tokens: 177,596; completion tokens: 249,443; reasoning subset: 222,525; cached prompt subset: 14,918.

## Per-call accounting

| Call | Completed | USD cost | Input | Completion | Reasoning subset | Client seconds | Provider | Finish |
|---|---|---:|---:|---:|---:|---:|---|---|
| section_01 | True | 0.00198896 | 9078 | 2707 | 2110 | 16.935 | Relace | stop |
| section_02 | False | 0.016893918 | 12613 | 32768 | 32768 | 108.042 | Relace | length |
| section_02_compact_v2 | True | 0.00680904 | 6144 | 6570 | 5287 | 22.247 | Fireworks | stop |
| section_02_compact_v2_repair | True | 0.0066211404 | 7545 | 7469 | 6058 | 23.082 | Fireworks | stop |
| section_03_compact_v2 | True | 0.0031357956 | 2816 | 3107 | 2414 | 12.576 | Fireworks | stop |
| section_04_compact_v2 | True | 0.0110626488 | 9319 | 10917 | 9408 | 35.657 | Fireworks | stop |
| section_05_compact_v2 | True | 0.009547104 | 8160 | 9404 | 7983 | 29.271 | Fireworks | stop |
| section_06_compact_v2 | False | 0.029347794 | 8993 | 32768 | 24710 | 74.99 | Fireworks | length |
| section_06_split_v3 | False | 0.028523586 | 5078 | 32768 | 28432 | 74.678 | Fireworks | length |
| section_07_split_v3 | True | 0.0073938228 | 5744 | 7448 | 6444 | 24.197 | Fireworks | stop |
| section_08_split_v3 | True | 0.010845324 | 7534 | 11106 | 9833 | 35.037 | Fireworks | stop |
| section_09_split_v3 | True | 0.007399644 | 5494 | 7514 | 6559 | 26.374 | Fireworks | stop |
| section_10_split_v3 | True | 0.0024095988 | 2170 | 2403 | 2099 | 10.156 | Fireworks | stop |
| stage1 | True | 0.01213937 | 52291 | 16958 | 12884 | 103.617 | Relace | stop |
| stage2 | False | 0.03519119 | 34617 | 65536 | 65536 | 226.31 | Relace | length |

## Outcome and limits

- Captures: 9 accepted analyses out of10; source coverage38/38 physical pages. The incomplete pages22–24 were supplied directly to Stage1, without synthetic section answers/ledger closures. Final ledger: 12 questions, {'resolved': 2, 'partial': 4, 'open': 6}; validation attempts {'rejected': 1, 'valid': 9}.
- Full Stage1 and full Stage2 were requested. Stage1 completed; do not equate completion with independent financial validation. Full Stage2 did not complete; see its receipt and `outputs/execution_outcome.json`. No recovery brief was requested or substituted.
- Initial section2 failed at32768 completion tokens, all reported as reasoning, no final answer. Its ID, usage and cost were preserved. Compact_v2 reduced section prompt workload and questions to four per capture without changing thinking/routing or raising token ceilings. Analytical prose and authoritative repaired ledger blocks are both retained.
- Generation metadata was initially unavailable (404 immediately after completion) but can become available later. Response usage cost is authoritative recorded cost here; later metadata corroborates it. Missing metadata is not zero cost.
- Prior NTU observed duration: 1996.07s; recorded successful-call elapsed: 373.44s. Prior failed calls lack complete accounting, so no reliable total-cost or active-time improvement can be claimed.
- Multiple prompt/question/settings changes and mixed pilot revisions prevent attributing the outcome solely to removing Nitro or changing reasoning.
- No current market quote, new PDF evidence, Gemini API call or production guardrail amendment was part of this run.

## Artifacts

- `plan.json`: authorization, settings, budgets, revisions and source provenance.
- `calls.csv`, `metrics.json`, `receipts/`: per-call and total cost/token/timing data, including failure.
- `requests/`, `outputs/`, `experiment.sqlite`: exact new requests, available answers, ledger and execution outcome.
- `inputs/`: preserved baseline outputs/requests, source text, review lessons, questions and production snapshot.
- `preservation.json`: all production tables, source PDF and enumerated originals unchanged.
- `gemini/PROMPT.md`: manual Antigravity review instructions.
