# NTU 1H26 — Stage2 300,000-token comparison

Decision: insufficient evidence for financial validation. This is a completion-limit experiment.

Exact saved Stage2 messages, model, temperature and streaming were retained. Only max_tokens=300000 was added. Default thinking and normal routing retained; provider may differ. One generation; no automatic paid retry. Original inputs preserved in inputs/ with SHA-256 manifest in plan.json. Source PDF and all production tables checked in preservation.json.

Known inherited error: Stage1 claims R370m portfolio cash discrepancy; prior executed Codex reconciliation yields R6m unexplained. This run does not correct its input. No new primary PDF inspection or current market quote; forecast/valuation/financing calculations NOT VERIFIED. No target or recommendation promoted. Gemini review remains manual in Antigravity. No sector_guardrails changes.

Prior evidence review: ../20261028T145027Z_codex_logical_trial_review/audit.md.

Transport and accounting results:
```json
{
  "model": "deepseek/deepseek-v4.1-flash-1017",
  "reasoning": "model default; controls omitted",
  "rows": [
    {
      "label": "stage2",
      "generation_id": "gen-1793201532-XYrLv1o6agOsBZ8doOXx",
      "success": false,
      "cost_usd": 0,
      "cost_source": "generation_metadata",
      "prompt_tokens": 35325,
      "completion_tokens": 183036,
      "reasoning_tokens": 183036,
      "cached_prompt_tokens": 0,
      "estimated_nonreasoning_completion_tokens": 0,
      "elapsed_seconds": 786.281,
      "time_to_first_content_seconds": null,
      "provider": "Relace",
      "generation_time_ms": 784898,
      "latency_ms": 1906,
      "finish_reason": null,
      "metadata_status": "retrieved"
    }
  ],
  "totals": {
    "cost_usd": 0,
    "prompt_tokens": 35325,
    "completion_tokens": 183036,
    "reasoning_tokens": 183036,
    "cached_prompt_tokens": 0,
    "elapsed_seconds": 786.281
  },
  "missing_fields_by_call": {
    "cost_usd": 0,
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "reasoning_tokens": 0,
    "cached_prompt_tokens": 0,
    "elapsed_seconds": 0
  },
  "calls": 1,
  "successful_generations": 0,
  "observed_first_dispatch_to_last_accounting_seconds": 793.094146,
  "notes": [
    "Reasoning tokens are part of completion tokens, not additional tokens.",
    "Known cost subtotal is not a complete bill when any cost is missing.",
    "Client elapsed, provider generation time and provider latency are distinct; check provider metadata units.",
    "Provider/account routing defaults may affect routing; no speed or priority override was sent."
  ]
}
```

Offline review: request equality/one-call accounting/source and production preservation checks passed. Preliminary StockEvaluator ran against explicit new note on a copied database with network disabled; see outputs/preliminary_evaluator.json. Historical bridge independently re-executed from prior verified inputs: net portfolio cash434 minus income246 equals carrying decline188; statutory182 leaves6 unexplained. See outputs/independent_calculations.json. No financial validation of Stage2 forecasts/valuation; Gemini review pending.

Final experiment finding:183036 reported completion/reasoning tokens exceeded prior131072 but fell below requested300000. Provider SSE502 provider_unavailable; both finish reasons null, no final answer. Reported costUSD0 verified with metadata-only refresh. Effective default-limit source and exact reason for provider unavailability NOT VERIFIED. Decision: insufficient evidence for financial validation; incomplete process. No retry. Original receipt preserved. Live dispatch tool exit1; offline review exit0.
