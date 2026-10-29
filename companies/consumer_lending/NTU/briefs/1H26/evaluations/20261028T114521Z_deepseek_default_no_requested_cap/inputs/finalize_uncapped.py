"""Finalize the authorized uncapped continuation; no model calls."""
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sqlite3
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('runner',HERE/'rerun.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
run=Path(m.POINTER.read_text(encoding='utf-8').strip())
plan=m.read(run/'plan.json');status=m.read(run/'status.json')
assert plan['section_prompt_revision']=='uncapped_v4'
assert status['status'] in {'completed_awaiting_independent_review','stopped'}
m.summarize(run);m.preserve(run)
metrics=m.read(run/'metrics.json');parent=Path(plan['parent_run']);parent_metrics=m.read(run/'inputs/parent_metrics.json')
receipts=[m.read(p) for p in sorted((run/'receipts').glob('*.json'))]
for r in receipts:
    payload=m.read(run/'requests'/f'{r["label"]}.json')
    assert not {'max_tokens','max_completion_tokens','reasoning','reasoning_effort','provider','service_tier'} & payload.keys()
    assert payload['model']==m.MODEL
new_cost=sum(Decimal(str(r['cost_usd'])) for r in receipts if r.get('cost_usd') is not None)
combined=new_cost+Decimal(str(parent_metrics['totals']['cost_usd']))
source=sqlite3.connect((run/'experiment.sqlite').as_uri()+'?mode=ro',uri=True)
count,accepted=source.execute('SELECT count(*),sum(llm_response IS NOT NULL) FROM sections').fetchone()
source.close()
success=status['status']=='completed_awaiting_independent_review'
shutil.copytree(parent/'outputs',run/'inputs/parent_outputs',dirs_exist_ok=True)
manifest=[]
for directory in ['requests','outputs','receipts','inputs/parent_outputs']:
    for p in sorted((run/directory).glob('*')):
        if p.is_file(): manifest.append(dict(path=str(p.relative_to(run)),sha256=m.sha(p)))
m.save(run/'inputs/audit_manifest.json',dict(recorded_utc=m.utc(),files=manifest,source_documents=plan['documents'],parent_inputs_preserved=True))
record=dict(recorded_utc=m.utc(),status=status,model=m.MODEL,no_caller_token_limit_fields=True,
 reasoning='Model default; controls omitted',routing='Base model; no Nitro/speed/provider-priority override',
 new_cost_usd=str(new_cost),new_cost_missing_calls=metrics['missing_fields_by_call']['cost_usd'],
 prior_capped_cost_usd=str(parent_metrics['totals']['cost_usd']),combined_recorded_cost_usd=str(combined),
 new_metrics=metrics,accepted_capture_count=accepted,active_capture_count=count,source_pages=38,
 preservation=m.read(run/'preservation.json'),financial_validation='Independent Gemini/Codex evidence review pending')
m.save(run/'completion_record.json',record)
lines=['# NTU — no caller-set completion-token cap','',
 ('**Full Stage1 and Stage2 generations completed.** Independent financial validation remains pending.' if success else '**Continuation stopped incomplete.** See status/receipt; do not infer a completed valuation.'),'',
 f'- Model: `{m.MODEL}`. Default thinking, normal routing. No max_tokens or max_completion_tokens sent; provider/model limits still apply.',
 f'- New attempts: {metrics["calls"]}; completed generations: {metrics["successful_generations"]}. Accepted capture analyses: {accepted}/{count},38/38 source pages.',
 f'- New recorded cost: **USD{new_cost}**; missing cost fields: {metrics["missing_fields_by_call"]["cost_usd"]}.',
 f'- Previous capped experiment: USD{parent_metrics["totals"]["cost_usd"]}; combined recorded cost: **USD{combined}**.',
 f'- New input tokens: {metrics["totals"]["prompt_tokens"]:,}; completion tokens: {metrics["totals"]["completion_tokens"]:,}; reasoning subset: {metrics["totals"]["reasoning_tokens"]:,}; cached-input subset: {metrics["totals"]["cached_prompt_tokens"]:,}.',
 f'- First dispatch to last accounting: **{metrics["observed_first_dispatch_to_last_accounting_seconds"]:.2f}s**; summed generation elapsed: **{metrics["totals"]["elapsed_seconds"]:.2f}s**.',
 '- All earlier failed attempts are preserved in the parent run. Nine accepted section analyses were reused; only the outstanding capture and downstream stages were regenerated (plus any explicitly logged repair).',
 '- Actual provider, native tokens, costs, finish reasons, cache usage, client timing and generation metadata are in `receipts/`, `calls.csv` and `metrics.json`.',
 '- Reasoning tokens are part of completion totals. Costs are summed once per generation. Missing accounting fields remain unknown, not zero.',
 '- Removing a requested cap does not provide infinite context/output or eliminate provider defaults. Different provider choices and generation variability prevent attributing completion solely to the cap change.',
 '- Production database tables, source PDF and enumerated parent outputs remain unchanged; see `preservation.json`.',
 '- No current market quote or Gemini API call. App publication assessment is not independent financial validation.',
 '', '## Review artifacts','',
 '- `outputs/stage1.md`, `outputs/stage2.md` (when completed), `outputs/stage2_publication.md`, `outputs/publication_assessment.json`.',
 '- `inputs/parent_outputs/` retains prior accepted/rejected outputs; `inputs/audit_manifest.json` hashes exact review files.',
 '- `gemini/PROMPT.md`: manual Antigravity review instructions.']
m.text(run/'RUN_SUMMARY.md','\n'.join(lines)+'\n')
m.text(run/'gemini/PROMPT.md',f'''Review NTU1H26 DeepSeek continuation at {run} in Antigravity. No paid model calls or production writes.
Read AGENTS.md, workflow/STATE.md, workflow/WORKFLOW.md, TOOL_CHEATSHEET.md and docs/STOCK_EVALUATION_FORMAT.md section1A. Save a new UTC-versioned Gemini evidence audit with exact inputs/hashes, independently executed calculations and actual outputs, physical-page coverage, C/F register, revisions and limitations. Preserve originals; inspect scripts before executing because hard-coded writes can modify prior evidence.
Read RUN_SUMMARY.md, plan.json, completion_record.json, metrics.json, calls.csv, receipts and preservation.json. Nine accepted prior capture analyses were reused; the outstanding pages22–24 capture, Stage1 and Stage2 were rerun with no caller-set token limit. No reasoning/routing override: default thinking, base model, no Nitro. Model/provider/account limits remain. Parent run{parent} retained four incomplete attempts and its costs; costs here are incremental and combined totals are separately labelled. Do not count reasoning twice.
Read exact new and parent accepted/rejected/effective section outputs, the complete ledger, raw Stage1/Stage2 and app publication assessment. App success does not validate finance. Source PDF:{plan['documents'][0]['path']}; SHA256:{m.SHA};38 physical pages. Reopen primary PDF tables/images. R0.89 is a frozen reference, not a current quote. Check signed POCI, both portfolio/cash bridges and residual6, signed amortisation, net receivables107, ETR signs, NAV/closing shares versus EPS, half/full-year impairment259, facility/overdraft/renewal scope, conditional simplified-ECL policy, and NCA/ABS applicability. The old Stage1 had contradictory ETR/staging prose; test whether refreshed output corrects it. Do not infer issuer forecasts are mandatory or accept all immateriality claims without quantified reasoning.
Independently reconstruct all actual forecasts, debt/cash/portfolio schedules, valuation components, lease treatment, terminal financing, sensitivity and readiness evidence. Distinguish numerical arithmetic, assumptions and missing evidence. Withhold any unsupported material target/recommendation; no invented replacement price. Grade unperformed checks NOT APPLICABLE, not PASS. Record corrected, remaining and newly introduced DeepSeek errors, evaluator reliability and prioritized prompt/ledger improvements. Propose rules for explicit approval; do not codify. Compare generation completeness separately from quality; variable providers/revisions limit causal conclusions. Codex will independently review your preserved Gemini audit.
''')
print(json.dumps(dict(status=status['status'],incremental_cost_usd=str(new_cost),combined_cost_usd=str(combined),metrics=metrics['totals'],elapsed=metrics['observed_first_dispatch_to_last_accounting_seconds'])))
