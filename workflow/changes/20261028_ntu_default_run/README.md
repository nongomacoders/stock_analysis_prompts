# NTU default-thinking, standard-routing rerun

User requested a fresh NTU run with lessons learned, without Nitro, at default thinking, with full cost/token/time accounting. The experiment is isolated from production valuations and original evidence.

Run directory: `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T101309Z_deepseek_default_standard/`. `latest_run.txt` points to it. Exact settings, authorization, evidence hashes and scope are in its `plan.json`; exact requests are saved before dispatch.

## Configuration

- Base model `deepseek/deepseek-v4.1-flash-1017`; no `:nitro`, provider sort/order or service-tier override. Account/provider routing defaults can still apply; inspect the actual provider in receipts.
- Reasoning controls omitted entirely. The catalog retrieved at run time reports thinking enabled by default, default effort `high`; this is not an explicit `medium`, `none` or `max` request. Sampling temperature0.1 retained from the prior trial.
- Nine existing captures cover all38 physical pages. Reuse source captures, not their analysis. Fresh scoped questions, validated persistent ledger, reviewed applicability/accounting lessons and the approved simplified-ECL registry rule.
- Planned eleven generations: nine sections, Stage1, Stage2. Two-section pilot first. Completion ceilings32,768/49,152/65,536 respectively; one ledger repair at most per section, no completion-budget escalation or automatic transport retries. Stop on failed repair/incomplete generation for diagnosis. No silent fallback that marks failed ledger answers successful.
- Full source text is supplied to Stage2. R0.89 is a frozen reference, not a live quote. Publication readiness assessment remains mandatory; independent financial validity still requires Gemini/Codex review.
- This changes multiple factors (lessons/questions/reasoning/routing/output instructions), so it cannot isolate a causal speed/quality effect of routing alone.

## Accounting

`rerun.py` uses streaming to capture IDs immediately and usage at stream completion. It persists receipts before completeness/ledger checks, including failed/truncated calls; raw reasoning is discarded. It queries the generation endpoint for billing/timing/provider metadata without generating another model answer. No credentials are written to artifacts or output.

Per-call fields include UTC dispatch/completion, local elapsed, response-header latency, first-event and first-visible-content times, finish reason, actual model/provider, prompt/completion/reasoning/cache tokens, USD cost and source, generation ID and provider timing/metadata. Reasoning is a subset of completion usage and is not added twice. `calls.csv` is the compact export; `metrics.json` retains totals and missing-field counts. Missing billing data remain unknown, not zero; usage cost and generation metadata are both retained rather than summed twice.

`inputs/production_snapshot.sqlite` and original file hashes preserve prior state; `preservation.json` checks every production table, source PDF and enumerated original outputs after execution. Pipeline writes target only `experiment.sqlite`.

## Local verification and references

Seven offline runner checks passed, exit0: default controls/base model, streaming usage/ID, ignoring raw reasoning, failed-call persistence, failure cost inclusion, no double-counting reasoning, and row-factory-independent logical snapshots. See `offline_checks.json`; simulated data are under `offline_check/` and are never included in live totals. No full pytest suite or global application change was required for this isolated runner.

Official references checked28 October2026:

- [Per-model defaults and reasoning controls](https://openrouter.ai/docs/guides/best-practices/reasoning-tokens).
- [Usage accounting](https://openrouter.ai/docs/cookbook/administration/usage-accounting): usage automatically included; deprecated include flags not needed.
- [Generation metadata](https://openrouter.ai/docs/api/api-reference/generations/get-request-&-usage-metadata-for-a-generation).
- [Provider routing](https://openrouter.ai/docs/guides/routing/provider-selection).

Gemini remains manual in Antigravity; no Gemini API calls are included. Other proposed production guardrail amendments are not implemented by this trial.

## Pilot revision

The initial section2 generation hit32,768 completion tokens, all reported as reasoning, and returned no final answer. It costUSD0.016893918 and took108.042 client seconds. The runner stopped (exit1), preserving its receipt. Section1 completed successfully. Default thinking therefore does not guarantee completion by itself.

Before resuming, preserved the original plan/status/runner and added `compact_v2`: replace the inherited multi-page section instructions with a concise section contract, four relevant questions per capture and four applicable registry rules. All open records remain in the complete Stage1 ledger. No source text was discarded; model, default thinking, normal routing and completion ceilings stayed unchanged. Section2 prompt length fell from59,627 to30,867 characters; its new generation completed in22.247 seconds, followed by one23.082-second ledger-only quote repair. Pilot then exited0. All three section2 calls remain in accounting.

Generation metadata lookups returned404 immediately after some completed calls; a later read retrieved their records successfully. Costs were already available in response usage. `refresh_billing.py` retries only metadata lookups, never model generation; this avoids paying again simply to recover accounting. `check_billing_lookup.py` preserved a diagnostic example. Provider times use the API's milliseconds; client timings use seconds.

## Final capped result and explicitly authorized continuation

The capped trial ultimately recorded15 attempts (11 completed generations,4 incomplete), costingUSD0.1893089364. Stage1 completed; full Stage2 hit65,536 tokens entirely in reported reasoning with no final answer. Parent audit/summary/receipts preserve this incomplete outcome. It must not be relabelled a completed financial withholding decision.

After the user explicitly requested rerunning incomplete sections with no token limit, `prepare_uncapped.py` created `20261028T114521Z_deepseek_default_no_requested_cap`, reusing nine accepted captures. No max_tokens/max_completion_tokens or reasoning/routing override was sent. Three generations completed without repair: outstanding capture, refreshed Stage1 and full Stage2. Incremental costUSD0.04537836; combinedUSD0.2346872964. New first-dispatch-to-last-accounting168.801s; summed request152.476s. Input89,445; completion38,498 including reasoning29,835. Final billing, omission, null-publication-field and preservation checks passed, exit0.

Full Stage2 returned a completed WITHHELD report, without forecasts/DCF/target. New generation completeness is established; valuation quality is not. New outputs fit below former ceilings and providers/context changed, so do not attribute success solely to cap omission. Provider/model limits still apply. See the continuation's `audit.md`, `RUN_SUMMARY.md`, `completion_record.json`, `metrics.json`, `calls.csv` and `gemini/PROMPT.md`. Current `latest_run.txt` points to the continuation; `previous_capped_run.txt` retains the parent path. No further paid calls, Gemini API calls, production edits or new guardrails were required.
