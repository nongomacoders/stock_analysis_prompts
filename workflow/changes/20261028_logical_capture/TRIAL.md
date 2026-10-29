# Reviewed NTU plan and gated DeepSeek trial

Authorized by the user's “proceed” after the plan-review/pilot/full-run proposal.
Run: `companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T141038Z_deepseek_reviewed_logical/`.
`trial_run.txt` points to it. Source PDF hash remains
`9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc`.

## Plan review

The automatic draft30 units became a reviewed24-unit plan by joining income/OCI/
equity statements (9–11), EPS (18–19), fair-value disclosures (27–29), and company/
back-cover information (37–38). The source text/pages are unchanged. These are
NTU-specific reviewed overrides, not hard-coded ranges in the general planner.
Same-period segment statement/reconciliation pairs have explicit H1/FY labels.

Two navigation/contact units (1–2,37–38) remain captured and available to later
stages but do not receive standalone model calls.22 financial units are analyzed,
then Stage1 and Stage2. Coverage remains38/38 physical pages exactly once. The
full ledger is fresh and processed in source order; pilot answers are not imported.

## Pilot and gate

Separate pilot database and ledger, with captures21–23,24 and25. Model: base
DeepSeek snapshot,default thinking,normal routing,no caller-set token ceiling.
Provider/model/account limits still apply. Exact payloads/receipts are saved.

Three initial captures completed. One required a retained quote repair. Independent
historical checks supported signed POCI gain, FY25 historical loss259 and conditional
trade-ECL interpretation. However, the first page25 answer incorrectly described it
as trade-table-only, missing the currency-risk note starting lower on that page.
A newly created question also duplicated a resolved POCI issue.

Before the full run, added run-only explicit secondary-heading context, a compact
resolved-ID index and short exact quote locators. One focused page25 recheck then
included USD/GBP exposure,60-day terms,FX hedging and Pending continuation to26,
with valid ledger JSON and no repair/new duplicate. Original answers/charges remain.
Pilot gate and revision evidence: `pilot/semantic_review_v1.json` and
`pilot/semantic_review.json`.

Five paid pilot generations totalUSD0.0340914924: three original captures,one quote
repair,one scope recheck. This is not five source captures. Scope/quote/index changes
are run-specific and do not amend production guardrails or global prompt defaults.

## Full chronological trial and accounting

24 planned generations:22 financial units plus Stage1/Stage2. Navigation units
remain explicitly captured without invented model answers or ledger closures.
The transport saves IDs,usage,costs and timing before completeness/ledger checks;
incomplete attempts and repairs remain chargeable records. Reasoning tokens are a
subset of completion tokens. Metadata lookups can be delayed; they are not paid
generation retries.

Exact execution versions are preserved in the run's inputs directory, including
driver before the pilot and driver/engine at full dispatch. `report_trial.py`
enriches generation metadata, writes full/pilot/combined accounting, checks source
and production preservation, executes `StockEvaluator.audit` against the explicit
experimental note on a database copy with networking disabled, and prepares the
manual Antigravity prompt. It never calls a model or requests a current quote.

The Stage1 exporter includes captured source text. The trial engine additionally
annexes navigation text for clarity; this duplicates some administrative context
and is not a minimal-token benchmark. Account for actual measured input tokens.
Different providers,prompts,groupings and ledger states prevent attributing cost or
quality changes to splitting alone. Independent financial validation remains
separate from generation completeness,source-page coverage and literal matching.

No Gemini API calls. Original outputs,source PDF and all production database tables
are preserved. Follow the run's `status.json`,then `RUN_SUMMARY.md` and
`combined_metrics.json` for actual final results,not planned counts.

## Actual final result

All22 financial captures completed in source order with valid literal ledger updates
and zero full-run repairs. Stage1 completed. Full Stage2 then stopped at131,072
completion tokens,all reported reasoning,no final answer; no token-cap field was
sent. This is an observed upstream limit,not proof of a globally unlimited request
or a specific provider/router/account configuration. No paid retry/recovery followed.

Full attempt24 generations (23 complete,1 incomplete),USD0.2445611328;
pilot5 generations,USD0.0340914924;combinedUSD0.2786526252. All29 costs matched
generation metadata. Full wall19m12.42s,summed request17m7.97s. Full input193,159;
completion312,161 including reasoning284,949. Source PDF,production tables and
prior outputs were unchanged.

Stage1 introduced an unsupportedR370m portfolio-cash comparison. Signed/scoped
net cash434 less accounting income246 equals carrying decline188;statutory182
leaves6 unexplained. This was first observed in Stage1,not earlier section briefs.
It is not known whether the error affected Stage2 reasoning;no Stage2 answer exists.
Do not attribute token exhaustion to it without evidence.

Separate preserved Codex review:
`companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T145027Z_codex_logical_trial_review/audit.md`.
The main run's manual Gemini prompt explicitly identifies available outputs,missing
Stage2,source evidence and this regression. No financial guardrail was codified.
The meaningful next engineering candidates are deterministic Stage1 reconciliation
and smaller linked Stage2 tasks,not a claim that sectioning alone fixes synthesis.
