"""Retry only delayed metadata lookups; never generate/resubmit a model answer."""
import importlib.util
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('runner',HERE/'rerun.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
from section_capture.openrouter import get_openrouter_api_key
run=Path(m.POINTER.read_text(encoding='utf-8').strip());key=get_openrouter_api_key()
for path in sorted((run/'receipts').glob('*.json')):
    r=m.read(path)
    if not r.get('completed_utc') or r.get('metadata_status')=='retrieved': continue
    m.metadata(run,r['label'],r,key)
    if r.get('cost_usd') is None:
        value=r.get('generation_metadata',{}).get('total_cost')
        if value is not None: r['cost_usd']=value;r['cost_source']='generation_metadata'
    m.save(path,r)
    print(r['label'],r['metadata_status'])
m.summarize(run)
