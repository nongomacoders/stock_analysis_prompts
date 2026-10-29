"""Preserve the pilot failure, reduce section workload, keep default settings/budgets."""
import importlib.util
import json
from pathlib import Path
import shutil
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('runner',HERE/'rerun.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
run=Path(m.POINTER.read_text(encoding='utf-8').strip())
assert m.read(run/'receipts/section_02.json')['finish_reason']=='length'
assert not (run/'inputs/plan_v1.json').exists(),'Revision already prepared'
shutil.copy2(run/'plan.json',run/'inputs/plan_v1.json')
shutil.copy2(run/'status.json',run/'inputs/pilot_v1_status.json')
plan=m.read(run/'plan.json');plan['section_prompt_revision']='compact_v2'
plan['revisions']=[dict(utc=m.utc(),reason='Pilot section2 exhausted32768 tokens entirely in reasoning, no final answer.',
 changes='Run-only concise section contract, four relevant questions per capture, four applicable registry rules. Full ledger retained; full Stage1/2 registry unchanged.',
 unchanged='Base model, default thinking, routing, evidence, approved registry, token ceilings and one-repair limit unchanged.',
 prior_failure_preserved=True)]
m.save(run/'plan.json',plan)
shutil.copy2(HERE/'rerun.py',run/'runner_compact_v2.py')
m.save(run/'inputs/compact_revision_checks.json',dict(checked_utc=m.utc(),
 request_payload=m.request_payload('Check default settings',32768),default_controls_omitted=True,
 original_pilot_receipts_preserved=True,statement='Only section prompt workload reduced; no token budget escalation.'))
print('Prepared compact_v2; prior failed attempt retained and included in total cost.')
