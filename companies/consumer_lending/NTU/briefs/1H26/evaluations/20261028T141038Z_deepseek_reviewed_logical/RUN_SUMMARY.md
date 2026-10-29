# NTU reviewed logical-capture trial

Execution status: **stopped**. Stage2 publication status: **NOT_PUBLISHED_PROCESS_INCOMPLETE**. Independent financial review remains pending.

24 captured units cover38 pages exactly once.22 financial units are analyzed in chronological order;2 navigation/contact units remain captured without standalone calls. Pilot and full ledgers are separate.

| Phase | Generations | Successful | Cost USD | Input tokens | Completion tokens | Reasoning subset | First dispatch to last accounting | Summed request time |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Pilot + scope recheck | 5 | 5 | 0.03409149 | 21,717 | 36,668 | 32,013 | 359.51s | 132.05s |
| Full chronological run | 24 | 23 | 0.24456113 | 193,159 | 312,161 | 284,949 | 1152.42s | 1027.97s |

**Combined known cost: USD0.2786526252**; missing-cost calls:0. Reasoning is already included in completion tokens.

The first pilot needed one quote repair and missed a secondary note on page25. One revised scope check then correctly included currency risk and continuation to26. All earlier outputs/charges remain preserved. The full run starts with a fresh ledger; pilot responses are intentionally not imported.
Run-only prompt improvements: explicit secondary note headings, short literal evidence locators and a compact resolved-question index. Production guardrails/prompts/valuations were not rewritten.

Model: DeepSeek base snapshot,default thinking,normal routing; no requested token cap. Actual providers,finish reasons,usage,cost,cache and timing are in per-call receipts/CSV. Variable providers and multiple prompt/partition changes prevent isolated causal conclusions.
Full ledger: 17 records;{'open': 4, 'partial': 11, 'resolved': 2};validation attempts:{'valid': 22}. A literal quote does not by itself prove closure.

Prior versions used different evidence groupings and mixed retries; lower cost or better financial accuracy is not assumed from completion. Source PDF,all production tables and enumerated original outputs remain unchanged.

Artifacts: `REVIEWED_PLAN.md`, `combined_metrics.json`, `calls.csv`, `pilot/calls.csv`, exact `requests/outputs/receipts`, `inputs/review_subject_manifest.json`, `preservation.json`, and `gemini/PROMPT.md`.
