# NTU 1H26: max-reasoning comparison attempt

Outcome: **INSUFFICIENT EVIDENCE - FRESH GENERATION BLOCKED**.

Created UTC: 2026-10-27T17:19:21.989556+00:00. Local: 2026-10-27T19:19:21.989580+02:00. Evaluator: Codex (model identifier not exposed).

## Valuation scorecard

No fresh target, forecast, recommendation, or market quote was produced. Prior DeepSeek R0.55 target and its dependent rating remain NOT VERIFIED under the preserved Codex review. Do not publish or synchronize a replacement valuation from this attempt.

## Execution and preserved inputs

The local `.venv/Scripts/python.exe -u scratch/run_ntu_max_comparison.py` process exited **1**. Stage 1 requested `deepseek/deepseek-v4.1-flash-1017:nitro`, reasoning `max`, 65,536 combined completion tokens and a 900-second HTTP timeout. The existing client retried and fell back to the base model. Final error: `OpenRouter connection error (deepseek/deepseek-v4.1-flash-1017): <urlopen error [Errno 11001] getaddrinfo failed>`.

No generation ID, provider response, usage, cost, achieved reasoning tokens, or final answer was returned. Completion and billing are not verified. Stage 2 was never submitted. No permission elevation was requested: network is restricted and sandbox approval is disabled in this session. DNS failure establishes unavailable name resolution here; it does not establish an OpenRouter service outage.

`inputs/manifest.json` preserves paths/hashes for four original DeepSeek briefs and all files in the Gemini and Codex evaluation directories, including saved input model outputs and existing calculations. `inputs/analysis_snapshot.sqlite` is a consistent SQLite backup. `inputs/sections_and_ledger.json` records the two existing captured sections and report metadata; `inputs/guardrails.json` records the rule registry. The original source PDF hash matches SQLite and the prior baseline: `9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc`. The PDF has 38 physical pages. No new PDF pages were read/extracted/rendered in this attempt: execution stopped before Stage 2 extraction. Prior audit pages and calculations were preserved, not independently revalidated in this attempt. No prior calculation script was executed.

`outputs/NTU_1H26_stage1_forensic_prompt.md` is the exact prepared 176,400-character prompt using current guardrails and existing captured material/ledger. Evaluator conclusions were not added to this prompt. `status.json` confirms all preserved original files and the PDF remain unchanged. The production Stage 1/2 notes, valuation fields and source locations were not replaced. No application source code was changed. Pytest was not run for this evidence-preservation and live-execution attempt; no financial validation is inferred from prior passing tests.

## Core comparison design

Fresh Stage 1 uses the same two captured sections/ledger. Fresh Stage 2 uses the fresh Stage 1, the hash-verified primary PDF with physical page markers and a frozen R0.89 reference (historical model reference, not a current quote). No new SENS inputs exist in the inspected source folder. Save raw final answers and exact prompts alongside `.run.json` metadata; do not sanitize away evidence before comparison. Keep the comparison separate from the production valuation until reviewed.

This is a combined test of increased reasoning, updated guardrails, regenerated prompts, and stochastic/provider variation. It cannot establish a causal reasoning-only improvement. Section analysis is reused, not rerun; any upstream defects remain available to test whether Stage 1 reopens them. The configured model identifier is the same requested model family; actual provider/model service behavior is unverified without generation metadata.

## Claim register and comparison checklist

The baseline diagnoses below come from the preserved Codex audit; this attempt does not revalidate those diagnoses. Every fresh-run verdict is **NOT VERIFIED** because no answer was returned. Preserve these IDs in the next comparison.

| ID | Claim to test | Prior observation / expected evidence | Fresh verdict |
| --- | --- | --- | --- |
| C001 | POCI gain versus ECL reserve classification | Prior Codex C003: 3414+431=3845; 431 is cumulative gain, preserve source allowance label and amortised-cost/FVTPL scope; PDF pp.13,23-24 | NOT VERIFIED |
| C002 | Statutory ordinary NAV | Prior C004: 1329/780.651033 approximately R1.70; contributed capital alone is not NAV; pp.8,16 | NOT VERIFIED |
| C003 | Net run-off footnote signs | Prior C005: (728-383+167)+(116-30)=598 versus597; explain remaining1 rather than assert exact reconciliation; pp.13,31 | NOT VERIFIED |
| C004 | Valuation bridge and repeated discounts | Prior C007-C009: unsupported1479 add-back and repeated discounts; rebuild inputs rather than adopt Gemini R1.07 | NOT VERIFIED |
| C005 | FCFE accounting and collection signs | Prior C013: collection inflows, purchase outflows, consistent IFRS-versus-CODM starting point; no blind sign flip | NOT VERIFIED |
| C006 | Forecast cash roll-forward | Prior C014: FY26/FY27/FY28 unexplained532/810/840; every forecast period needs financing and balance-sheet reconciliation | NOT VERIFIED |
| C007 | Sensitivity reproduction | Prior C015: matrix must use exact base valuation formula and reproduce central target | NOT VERIFIED |
| C008 | Revenue denominator and scope | Prior C016: UK+US515/711=72.4% of IFRS services;515/1599=32.2% CODM total; p.36 | NOT VERIFIED |
| C009 | Liquidity claims and available facilities | Prior C012/C020:809 is partial static comparison, not a proven future shortfall; facilities and restrictions unresolved | NOT VERIFIED |
| C010 | Lifetime versus12-month ECL allegation | Prior C017: clarification warranted, understatement not established | NOT VERIFIED |
| C011 | Rating bands and trading-stop direction | Prior C010/C011/C021: economic target first; monotonic bands do not validate it; short stop must limit losses in correct direction | NOT VERIFIED |
| C012 | New errors or omissions | Check all fresh material dependencies, beyond this baseline checklist | NOT VERIFIED |

For each item, record Stage 1 treatment, Stage 2 treatment, primary-page evidence, independent calculations, severity, and whether the defect was corrected, persisted, newly introduced, or remains unverified. Distinguish correction from mere omission. Review Gemini's supported/partly supported findings and Codex-identified misses separately. Count only tested claims, and do not interpret more words or more reasoning tokens as proof of quality.

## Valuation errors and analytical lessons

No fresh valuation exists, so no new valuation error or quality improvement can be established. The preserved baseline still requires corrections; its target/rating cannot be adopted solely because checks run or models agree. No new reusable analytical rule was discovered or proposed in this execution attempt; no guardrail database codification is requested or performed.

## Decision and handoff

Resume using the saved runner from the repository root in an environment with working OpenRouter access:

```powershell
.venv/Scripts/python.exe -u scratch/run_ntu_max_comparison.py
```

It creates a new timestamped run and preserves current originals again, rather than altering this failed attempt. A copy of the exact executed runner is saved here as `run_comparison.py`; it expects execution from the project root and the original scratch runner to remain available for its final self-copy. Stage 1 must complete before Stage 2 starts. Both outputs and actual metadata must then be reviewed against primary evidence and the register above. No fresh results are available for Gemini review yet.

Revision log: initial attempt saved once after failed live Stage 1 request. No analytical finding was silently revised.
