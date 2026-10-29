"""Preserve the exact pre-refinement prompt files before authorized edits."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
items=[]
for sector in ['common','consumer_lending']:
    path=ROOT/f'prompts/{sector}/12-analyst-reading-brief/v1.1.0/prompt.md'
    dest=HERE/f'before_{sector}.md'
    if dest.exists():assert dest.read_bytes()==path.read_bytes(),'Before-copy already exists; inspect before modifying'
    else:dest.write_bytes(path.read_bytes())
    items.append(dict(path=str(path),saved=dest.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
(HERE/'before_manifest.json').write_bytes((json.dumps(items,indent=2)+'\n').encode('utf-8'))
print('Both pre-refinement prompts preserved.')
