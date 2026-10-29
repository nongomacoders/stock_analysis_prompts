"""Read accounting metadata only; no inference requests."""
from pathlib import Path
import importlib.util,sys,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('transport',ROOT/'workflow/changes/20261028_ntu_default_run/rerun.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
from section_capture.openrouter import get_openrouter_api_key
run=Path((HERE/'pilot_run.txt').read_text().strip());key=get_openrouter_api_key()
dest=run/'receipts_before_refresh';dest.mkdir(exist_ok=True)
for p in sorted((run/'receipts').glob('*.json')):
    receipt=m.read(p)
    if receipt.get('metadata_status')=='retrieved':continue
    shutil.copy2(p,dest/p.name)
    m.metadata(run,receipt['label'],receipt,key);m.save(p,receipt)
    print(receipt['label'],receipt['metadata_status'],flush=True)
m.summarize(run);metrics=m.read(run/'metrics.json');metrics['reasoning']='none/exclude=true';m.save(run/'metrics.json',metrics)
