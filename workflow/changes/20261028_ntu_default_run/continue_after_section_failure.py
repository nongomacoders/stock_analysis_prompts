"""Do not retry the failed section; explicitly annex its original source to Stage1."""
import importlib.util
from pathlib import Path
import shutil
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('runner',HERE/'rerun.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
run=Path(m.POINTER.read_text(encoding='utf-8').strip())
assert m.read(run/'receipts/section_06_split_v3.json')['finish_reason']=='length'
plan=m.read(run/'plan.json');assert not plan.get('continue_with_explicit_failed_section_source')
shutil.copy2(run/'plan.json',run/'inputs/plan_v3_before_coverage_continuation.json')
shutil.copy2(run/'status.json',run/'inputs/split_v3_stop_status.json')
plan['continue_with_explicit_failed_section_source']=True
plan['revisions'].append(dict(utc=m.utc(),reason='Smaller portfolio capture also incomplete at same ceiling; no further repeat/budget increase.',
 changes='Mark incomplete section analyses explicitly; apply no ledger updates and provide their original captured source directly to Stage1. Continue other captures and full analysis stages.',
 limits='This tests the end-to-end workflow with disclosed section-generation gaps; do not claim every section analysis succeeded.'))
m.save(run/'plan.json',plan);shutil.copy2(HERE/'rerun.py',run/'runner_explicit_incomplete_coverage.py')
print('Coverage continuation recorded; no failed section will be automatically resubmitted.')
