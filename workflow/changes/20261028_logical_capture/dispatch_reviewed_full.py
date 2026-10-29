"""Dispatch only after semantic pilot gate; preserve the exact revised driver/engine."""
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('trial',HERE/'trial.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
run=Path(t.POINTER.read_text(encoding='utf-8').strip())
assert t.m.read(run/'pilot/semantic_review.json')['gate']=='PASS'
plan=t.m.read(run/'plan.json')
plan['full_prompt_revision']='shared_topic_and_resolved_index_v2'
plan['pilot_scope_revision']='Original3 captures +1 ledger repair +1 page25 scope recheck; preserved separately'
plan['pilot_gate_passed']=True
t.m.save(run/'plan.json',plan)
shutil.copy2(HERE/'trial.py',run/'inputs/trial_driver_v2.py')
shutil.copy2(t.ENGINE,run/'inputs/transport_engine_at_full_dispatch.py')
print('Pilot passed; full chronological run uses a fresh ledger,22 analytical captures and2 stages.',flush=True)
raise SystemExit(subprocess.call([sys.executable,str(HERE/'trial.py'),'execute'],cwd=t.ROOT))
