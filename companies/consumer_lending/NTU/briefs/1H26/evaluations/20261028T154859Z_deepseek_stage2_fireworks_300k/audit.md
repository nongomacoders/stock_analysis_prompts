# NTU1H26 Fireworks Stage2 provider experiment

Decision: insufficient evidence for financial validation. One generation, pinned Fireworks, fallback disabled,300000 combined reasoning/final-answer tokens, default thinking controls omitted. Same exact input as Relace300k; only provider object changed. No production writes or other paid calls. Exact preserved input model outputs and request/engine/driver hashes:plan.json. Source PDF referenced by original path/SHA;no new PDF inspection.

Known inherited Stage1 error: allegedR370m portfolio discrepancy is unsupported; prior verified arithmetic leavesR6m unexplained. No input correction made for this provider comparison. Forecast/DCF/shares/financing/current market checks NOT VERIFIED pending independent review; no target/recommendation promoted. No new sector guardrails proposed. Prior primary-source Codex review:../20261028T145027Z_codex_logical_trial_review/audit.md.

Transport/accounting metrics:
```json
{
  "model": "deepseek/deepseek-v4.1-flash-1017",
  "reasoning": "model default; controls omitted",
  "rows": [
    {
      "label": "stage2",
      "generation_id": "gen-1793202549-WH7Nojp6J6BhWcpfHL8P",
      "success": true,
      "cost_usd": 0.02148888,
      "cost_source": "response_usage",
      "prompt_tokens": 35708,
      "completion_tokens": 16655,
      "reasoning_tokens": 11727,
      "cached_prompt_tokens": 0,
      "estimated_nonreasoning_completion_tokens": 4928,
      "elapsed_seconds": 50.43,
      "time_to_first_content_seconds": 38.837,
      "provider": "Fireworks",
      "generation_time_ms": null,
      "latency_ms": null,
      "finish_reason": "stop",
      "metadata_status": "unavailable"
    }
  ],
  "totals": {
    "cost_usd": 0.02148888,
    "prompt_tokens": 35708,
    "completion_tokens": 16655,
    "reasoning_tokens": 11727,
    "cached_prompt_tokens": 0,
    "elapsed_seconds": 50.43
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
  "successful_generations": 1,
  "observed_first_dispatch_to_last_accounting_seconds": 56.051579,
  "notes": [
    "Reasoning tokens are part of completion tokens, not additional tokens.",
    "Known cost subtotal is not a complete bill when any cost is missing.",
    "Client elapsed, provider generation time and provider latency are distinct; check provider metadata units.",
    "Provider/account routing defaults may affect routing; no speed or priority override was sent."
  ]
}
```

Offline review: request differs solely by explicit provider object;one generation;actual provider checked if returned;source/production/original files preserved. Preliminary StockEvaluator on explicit experimental path and copied DB with network denied. Historical arithmetic re-executed:434−246=188,minus statutory182=6 unexplained. New forecast/valuation dependencies NOT VERIFIED. Manual Gemini prompt saved;no Gemini API. Final measured results:
```json
{
  "provider": "Fireworks",
  "model": "deepseek/deepseek-v4.1-flash-20261017",
  "generation_id": "gen-1793202549-WH7Nojp6J6BhWcpfHL8P",
  "success": true,
  "finish_reason": "stop",
  "native_finish_reason": "stop",
  "elapsed_seconds": 50.43,
  "time_to_first_content_seconds": 38.837,
  "prompt_tokens": 35708,
  "completion_tokens": 16655,
  "reasoning_tokens": 11727,
  "cost_usd": 0.02148888,
  "original_receipt_cost_usd": 0.02148888,
  "api_error": null,
  "nonreasoning_tokens": 4928
}
```

Offline review: request differs solely by explicit provider object;one generation;actual provider checked if returned;source/production/original files preserved. Preliminary StockEvaluator on explicit experimental path and copied DB with network denied. Historical arithmetic re-executed:434−246=188,minus statutory182=6 unexplained. New forecast/valuation dependencies NOT VERIFIED. Manual Gemini prompt saved;no Gemini API. Final measured results:
```json
{
  "provider": "Fireworks",
  "model": "deepseek/deepseek-v4.1-flash-20261017",
  "generation_id": "gen-1793202549-WH7Nojp6J6BhWcpfHL8P",
  "success": true,
  "finish_reason": "stop",
  "native_finish_reason": "stop",
  "elapsed_seconds": 50.43,
  "time_to_first_content_seconds": 38.837,
  "prompt_tokens": 35708,
  "completion_tokens": 16655,
  "reasoning_tokens": 11727,
  "cost_usd": 0.02148888,
  "original_receipt_cost_usd": 0.02148888,
  "api_error": null,
  "nonreasoning_tokens": 4928
}
```

Tool retrospective: initial offline review exited1 when Python write_bytes to workflow/STATE.md returned OSError22 Invalid argument. State file remained intact. Review revised to stage a candidate; second offline review exit0. Native PowerShell WriteAllText applied the candidate successfully. No policy denial observed. Full-suite not rerun; application unchanged.
