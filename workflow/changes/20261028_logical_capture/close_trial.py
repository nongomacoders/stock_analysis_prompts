"""Finalize phase status and verify the sealed review; no model/network calls."""
import importlib.util
from pathlib import Path
import shutil
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('trial',HERE/'trial.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
m=t.m;run=Path(t.POINTER.read_text(encoding='utf-8').strip());pilot=run/'pilot'
audit=Path((HERE/'trial_audit.txt').read_text(encoding='utf-8').strip())
r=m.read(pilot/'receipts/page25_scope_recheck_v2.json')
status=m.read(pilot/'status.json');status.update(status='completed_after_semantic_review',stage='scope_recheck_complete',
    completed_utc=r['accounting_completed_utc'],semantic_gate='PASS',status_finalized_utc=m.utc())
m.save(pilot/'status.json',status)
target=audit/'inputs/pilot/status.json';shutil.copy2(pilot/'status.json',target)
manifest=m.read(audit/'inputs/manifest.json')
manifest['files'].append(dict(original=str(pilot/'status.json'),saved=str(target.relative_to(audit)),sha256=m.sha(target)))
m.save(audit/'inputs/manifest.json',manifest)
for row in manifest['files']:
    assert m.sha(Path(row['original']))==m.sha(audit/row['saved'])==row['sha256'],row['original']
m.preserve(run);m.preserve(pilot)
assert m.read(run/'status.json')['status']=='stopped'
with (audit/'audit.md').open('a',encoding='utf-8',newline='') as out:
    out.write('\nFinalization note: a multi-file documentation patch failed context verification before writing; bounded corrected hunks applied successfully. No policy/permission denial occurred. Pilot status was finalized from its saved last receipt and semantic gate; raw receipts/model outputs remained unchanged. Final manifest and production/source checks passed.\n')
m.save(run/'closure_checks.json',dict(checked_utc=m.utc(),all_review_manifest_hashes_match=True,
    production_source_and_originals_unchanged=True,active_generation=False,pilot_status='completed_after_semantic_review',
    full_status='stopped_incomplete_stage2',paid_calls_in_finalization=0))
print('Final manifests,statuses,source and production preservation verified; exit0; no paid calls.')
