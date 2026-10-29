# NTU Stage2 — explicit 300,000-token experiment

One paid-generation attempt on Relace, exact original messages/model/temperature/stream, with only max_tokens=300000 added. Default thinking and normal routing retained.

Result: INCOMPLETE. After786.281 seconds (13m6.281s), the SSE stream returned502 provider_unavailable ("JSON error injected into SSE stream"). HTTP response initially200; no terminal DONE event or final answer. Finish reasons null, not length. Provider generation time784898ms. Metadata reports35325 input tokens and183036 completion tokens, all reasoning; no cached input. Metadata currently reports total_cost USD0, corroborated by a separate metadata-only refresh. This is reported accounting, not independent invoice verification. Original receipt retained unchanged, including transient404 before successful metadata retrieval.

Comparison: previous Relace attempt ended length at131072 reasoning/completion tokens,286.947s,USD0.06803556. This attempt passed that observed token boundary but failed below the requested300000. The explicit larger cap allowed a longer generation in this comparison; it does not prove the router/provider's exact default, that300000 would be honored to completion, or the cause of provider unavailability. No final financial note exists. No retry was submitted.

Offline checks passed, exit0: only requested cap differs, exactly one attempt, all production tables/source PDF/original files unchanged, historical bridge re-executed (434−246=188 versus182 leaves6 unexplained). Preliminary evaluator MISSING_NOTE on explicit new path; it did not fall back to an old valuation. Dispatch command reported exit1; saved status incomplete. No full pytest rerun: application code unchanged; this was an isolated live experiment.

Known inherited Stage1 error (R370m alleged portfolio difference) remains uncorrected in the comparison input. No primary pages newly inspected, forecast/DCF/financing/market comparisons NOT VERIFIED, no target/recommendation published. No new financial guardrails proposed or codified. Audit: audit.md. Exact request, receipt, metrics, comparison and refreshed metadata are saved beside this summary.
