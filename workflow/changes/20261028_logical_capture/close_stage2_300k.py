"""Refresh metadata only, then record the completed single-attempt experiment."""
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('comparison',HERE/'stage2_300k.py')
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
m=t.m
run=Path(t.POINTER.read_text(encoding='utf-8').strip())
r=m.read(run/'receipts/stage2.json')
assert r['api_error']['code']==502 and r['api_error']['metadata']['error_type']=='provider_unavailable'
from section_capture.openrouter import get_openrouter_api_key
refreshed=dict(r)
m.metadata(run,'stage2',refreshed,get_openrouter_api_key())
m.save(run/'outputs/generation_metadata_refresh.json',dict(checked_utc=m.utc(),generation_metadata=refreshed.get('generation_metadata'),metadata_status=refreshed.get('metadata_status')))
g=refreshed['generation_metadata']
assert g['native_tokens_completion']==g['native_tokens_reasoning']==183036
assert g['native_tokens_completion']>131072 and g['native_tokens_completion']<300000
summary='''# NTU Stage2 — explicit 300,000-token experiment

One paid-generation attempt on Relace, exact original messages/model/temperature/stream, with only max_tokens=300000 added. Default thinking and normal routing retained.

Result: INCOMPLETE. After786.281 seconds (13m6.281s), the SSE stream returned502 provider_unavailable ("JSON error injected into SSE stream"). HTTP response initially200; no terminal DONE event or final answer. Finish reasons null, not length. Provider generation time784898ms. Metadata reports35325 input tokens and183036 completion tokens, all reasoning; no cached input. Metadata currently reports total_cost USD0, corroborated by a separate metadata-only refresh. This is reported accounting, not independent invoice verification. Original receipt retained unchanged, including transient404 before successful metadata retrieval.

Comparison: previous Relace attempt ended length at131072 reasoning/completion tokens,286.947s,USD0.06803556. This attempt passed that observed token boundary but failed below the requested300000. The explicit larger cap allowed a longer generation in this comparison; it does not prove the router/provider's exact default, that300000 would be honored to completion, or the cause of provider unavailability. No final financial note exists. No retry was submitted.

Offline checks passed, exit0: only requested cap differs, exactly one attempt, all production tables/source PDF/original files unchanged, historical bridge re-executed (434−246=188 versus182 leaves6 unexplained). Preliminary evaluator MISSING_NOTE on explicit new path; it did not fall back to an old valuation. Dispatch command reported exit1; saved status incomplete. No full pytest rerun: application code unchanged; this was an isolated live experiment.

Known inherited Stage1 error (R370m alleged portfolio difference) remains uncorrected in the comparison input. No primary pages newly inspected, forecast/DCF/financing/market comparisons NOT VERIFIED, no target/recommendation published. No new financial guardrails proposed or codified. Audit: audit.md. Exact request, receipt, metrics, comparison and refreshed metadata are saved beside this summary.
'''
m.text(run/'RUN_SUMMARY.md',summary)
with (run/'audit.md').open('a',encoding='utf-8',newline='') as f:
    f.write('\nFinal experiment finding:183036 reported completion/reasoning tokens exceeded prior131072 but fell below requested300000. Provider SSE502 provider_unavailable; both finish reasons null, no final answer. Reported costUSD0 verified with metadata-only refresh. Effective default-limit source and exact reason for provider unavailability NOT VERIFIED. Decision: insufficient evidence for financial validation; incomplete process. No retry. Original receipt preserved. Live dispatch tool exit1; offline review exit0.\n')
state=t.ROOT/'workflow/STATE.md'
body=state.read_text(encoding='utf-8')
marker='## Completed\n'
assert body.count(marker)==1
entry='''
- **NTU Stage2 explicit300k experiment finished incomplete (2026-10-28)**:
  - User authorized one300,000-token Stage2 rerun. Exact original prompt/model/temperature/stream retained; only max_tokens added. Default thinking and normal routing; actual provider Relace again. Run:`companies/consumer_lending/NTU/briefs/1H26/evaluations/20261028T153201Z_deepseek_stage2_300k/`.
  - Stream failed with502 provider_unavailable after786.281s (13m6.281s),no final answer,finish reasons null. Metadata183,036 completion tokens,all reasoning,input35,325;reportedUSD0 corroborated by metadata-only refresh. Passed prior131,072 observed stopping point but failed before300,000. This does not establish exact omitted-cap default or cause of upstream failure. No automatic retry.
  - Saved request/receipt/cost-time-token metrics,comparison,RUN_SUMMARY.md and versioned audit.md. Offline review exit0;dispatch tool exit1. Preliminary evaluator against explicit new path MISSING_NOTE;no production fallback or published valuation. All production tables/source PDF/original files verified unchanged. Historical bridge rerun leaves6 unexplained;known Stage1 R370m claim retained in unchanged comparison input. No app defaults,financial guardrails or Gemini calls changed;no full pytest rerun for isolated experiment.

'''
state.write_bytes(body.replace(marker,marker+entry,1).encode('utf-8'))
cheat=t.ROOT/'TOOL_CHEATSHEET.md'
with cheat.open('a',encoding='utf-8',newline='') as f:
    f.write('\n### 35. Explicit Cap Experiments and Midstream Provider Failures\n* Preserve identical request messages and all other controls when testing a larger token cap; compare actual providers. An initial HTTP200 can later contain an SSE502 provider_unavailable; null finish reasons are not length. Record no final answer and preserve accounting before interpreting failure. NTU300k passed131072 but failed at183036 reported reasoning tokens. Do not infer which default imposed the old cutoff or why the provider failed.\n* Metadata after a failed stream can report zero cost; retain its source and timestamp, refresh metadata separately without another completion, and distinguish reported accounting from invoice verification. Preserve transient404 history after successful metadata retrieval.\n* This turn repeated oversized document reads; section19 already covers bounded reads. No shell/encoding/edit failures were observed; the live command exit1 was a provider-stream failure, not a local permission error.\n')
m.preserve(run)
m.save(run/'closure_checks.json',dict(checked_utc=m.utc(),one_generation=True,request_only_max_tokens_changed=True,
    dispatched_command_exit_code=1,offline_review_exit_code=0,metadata_refresh=g,
    preservation=m.read(run/'preservation.json'),financial_validation='NOT VERIFIED',retry_submitted=False))
print(json.dumps(dict(run=str(run),metadata_cost=g.get('total_cost'),tokens=g['native_tokens_completion'],preservation=m.read(run/'preservation.json'))))
